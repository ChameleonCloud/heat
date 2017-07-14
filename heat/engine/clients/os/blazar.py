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

from heat.common import exception
from heat.engine.clients import client_plugin
from heat.engine import constraints

CLIENT_NAME = 'blazar'


class BlazarClientPlugin(client_plugin.ClientPlugin):

    service_types = [RESERVATION] = ['manager']

    def is_not_found(self, ex):
        return (isinstance(ex, exceptions.HTTPClientError) and
                ex.status_code == 404)

    def get_reservation_by_ref(self, reservation_ref):
        try:
            return reservation_ref
        except Exception as ex:
            if self.is_not_found(ex):
                raise exception.EntityNotFound(
                    entity="Reservation",
                    name=reservation_ref)
            raise


class ReservationConstraint(constraints.BaseCustomConstraint):
    expected_exceptions = (exception.EntityNotFound,)

    def validate_with_client(self, client, reservation):
        pass
