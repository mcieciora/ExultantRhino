pipeline {
    agent {
        node {
            label 'amy'
        }
    }
    stages {
        stage('Prepare for tests') {
            parallel {
                stage ('Verify requirements'){
                    steps {
                        script {
                            dir('automated_tests/tools') {
                                def reqs_verification = sh(script: 'python3.10 verify_requirements.py', returnStdout: true)
                                if (reqs_verification.contains('[ERR]')) {
                                    error("${reqs_verification}")
                                }
                            }
                        }
                    }
                }
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
                            sh "sed -i 's/mongodb/localhost/1' src/pymongo_db.py"
                            sh "sed -i 's/latest/4.4.6/1' docker-compose.yml"
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
                        sh 'tox -e unittests'
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
    }
    post {
        always {
            script{
                sh 'docker compose down'
                sh "docker rmi exultant_rhino_app -f"
            }
            archiveArtifacts artifacts: 'automated_tests/*results.xml', fingerprint: true
            junit 'automated_tests/*results.xml'
            cleanWs()
        }
    }
}