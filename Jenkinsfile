pipeline {

    agent {
        node {
            label 'amy'
        }
    }

    options {
        skipDefaultCheckout()
    }

    stages {
        stage('Stage') {
            steps {
                script {
                    def PWD_COMMAND = sh (script: 'pwd', returnStdout: true).trim()
                    echo "${PWD_COMMAND}"
                }
            }
        }
    }
}