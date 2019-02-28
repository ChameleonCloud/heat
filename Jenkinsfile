pipeline {
  agent any

  options {
    copyArtifactPermission(projectNames: 'heat*')
  }

  stages {
    stage('package') {
      environment {
        PBR_VERSION = "${env.BRANCH_NAME}"
      }
      steps {
        dir('dist') {
          deleteDir()
        }
        sh 'python setup.py sdist'
        sh 'find dist -type f -exec cp {} dist/heat.tar.gz \\;'
        archiveArtifacts(artifacts: 'dist/heat.tar.gz', onlyIfSuccessful: true)
      }
    }
  }
}
