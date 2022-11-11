pipeline {

    agent {
        node {
            label 'amy'
        }
    }

    stages {
        stage('Lint & Unit') {
            parallel {
                stage('Linting') {
                    steps {
                        script {
                            dir('automated_tests/') {
                                sh 'tox -e lint src'
                                sh 'tox -e lint automated_tests'
                            }
                        }
                    }
                }
                stage('Database unittests') {
                    steps {
                        script {
                            dir('automated_tests/') {
                                sh 'tox -e database_tests'
                            }
                        }
                    }
                }
            }

        }
    }
}