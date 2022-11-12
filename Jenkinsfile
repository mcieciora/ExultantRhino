pipeline {
    agent {
        node {
            label 'amy'
        }
    }
    stages {
        stage('Prepare for tests') {
            parallel {
                stage ('Code linting'){
                    steps {
                        script {
                            dir('automated_tests/') {
                                sh 'tox -e lint src'
                                sh 'tox -e lint automated_tests'
                            }
                        }
                    }
                }
                stage ('Setup docker image'){
                    steps {
                        script {
                            dir('automated_tests/') {
                                sh 'docker compose down'
                            }
                            def all_images = sh(script: 'docker images', returnStdout: true)
                            if (all_images.contains('exultant_rhino_app')) {
                                sh "docker rmi exultant_rhino_app -f"
                            }
                            sh "sed -i 's/mongodb/localhost/1' src/mongodb.py"
                            sh 'docker compose up -d'
                            }
                        }
                    }
                }
            }

        stage ('Unittests'){
            steps {
                script {
                    dir('automated_tests/') {
                        sh 'tox -e database_tests'
                    }
                }
            }
            post {
                always {
                    script {
                        sh 'docker compose down'
                        sh 'docker rmi exultant_rhino_app:latest -f'
                    }
                }
                failure {
                    script {
                        sh 'docker logs exultant_rhino_app'
                    }
                }
            }
        }

        stage ('Regular tests'){
            steps {
                script {
                    sh "sed -i 's/localhost/mongodb/1' src/mongodb.py"
                    sh 'docker compose up -d'
                    dir('automated_tests/') {
                        sh 'tox -e regression'
                    }
                }
            }
            post {
                failure {
                    script {
                        sh 'docker logs exultant_rhino_app'
                    }
                }
            }
        }
    }
    post {
        always {
            script{
                sh 'docker compose down'
                sh "docker rmi exultant_rhino_app -f"
            }
            archiveArtifacts artifacts: 'automated_tests/*results.xml,automated_tests/results.html', fingerprint: true
            junit 'automated_tests/*results.xml'
        }
    }
}