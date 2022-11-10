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
        stage('Stage 1') {
            steps {
                LS_COMMAND = sh (script: 'ls',returnStdout: true).trim()
                echo "${LS_COMMAND}"
            }
        }
    }
}