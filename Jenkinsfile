pipeline {

    agent {
        node {
            label 'amy'
        }
    }

    stages {
        stage('Stage') {
            steps {
                script {
                    dir('automated_tests/') {
                        sh 'tox -e lint src'
                        sh 'tox -e lint automated_tests'
                    }
                }
            }
        }
    }
}