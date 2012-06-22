# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
from novaclient.exceptions import BadRequest
from novaclient.exceptions import NotFound
from heat.common import exception
from heat.engine.resources import Resource

logger = logging.getLogger('heat.engine.security_group')


class SecurityGroup(Resource):
    properties_schema = {'GroupDescription': {'Type': 'String',
                                              'Required': True},
                         'VpcId': {'Type': 'String',
                                   'Implemented': False},
                         'SecurityGroupIngress': {'Type': 'List'},
                         'SecurityGroupEgress': {'Type': 'List',
                                                  'Implemented': False}}

    def __init__(self, name, json_snippet, stack):
        super(SecurityGroup, self).__init__(name, json_snippet, stack)

    def handle_create(self):
        sec = None

        groups = self.nova().security_groups.list()
        for group in groups:
            if group.name == self.name:
                sec = group
                break

        if not sec:
            sec = self.nova().security_groups.create(self.name,
                                          self.properties['GroupDescription'])

        self.instance_id_set(sec.id)
        if 'SecurityGroupIngress' in self.properties:
            rules_client = self.nova().security_group_rules
            for i in self.properties['SecurityGroupIngress']:
                try:
                    rule = rules_client.create(sec.id,
                                               i['IpProtocol'],
                                               i['FromPort'],
                                               i['ToPort'],
                                               i['CidrIp'])
                except BadRequest as ex:
                    if ex.message.find('already exists') >= 0:
                        # no worries, the rule is already there
                        pass
                    else:
                        # unexpected error
                        raise

    def handle_delete(self):
        if self.instance_id is not None:
            try:
                sec = self.nova().security_groups.get(self.instance_id)
            except NotFound:
                pass
            else:
                for rule in sec.rules:
                    try:
                        self.nova().security_group_rules.delete(rule['id'])
                    except NotFound:
                        pass

                self.nova().security_groups.delete(sec)
            self.instance_id = None

    def FnGetRefId(self):
        return unicode(self.name)
