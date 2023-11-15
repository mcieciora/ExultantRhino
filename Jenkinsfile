def customImage

pipeline {
    agent any
    environment {
        FLAG = getTestEnvValue()
    }
    stages {
        stage ("Prepare docker test image") {
            steps {
                script {
                    customImage = docker.build("test_image:${env.BUILD_ID}", "-f automated_tests/Dockerfile .")
                }
            }
        }
        stage("Code analysis") {
            parallel {
                stage ("Pylint") {
                    steps {
                        script {
                            customImage.inside("-v $WORKSPACE:/app") {
                                sh "python3 -m pylint src --max-line-length=120 --disable=C0114 --fail-under=9.5"
                                sh "python3 -m pylint --load-plugins pylint_pytest automated_tests --max-line-length=120 --disable=C0114,C0116 --fail-under=9.5"
                            }
                        }
                    }
                }
                stage ("flake8") {
                    steps {
                        script {
                            customImage.inside("-v $WORKSPACE:/app") {
                                sh "python3 -m flake8 --max-line-length 120 --max-complexity 10 src"
                            }
                        }
                    }
                }
                stage("Code coverage") {
                    steps {
                        script {
                            customImage.inside("-v $WORKSPACE:/app") {
                                sh "python3 -m pytest --cov=src automated_tests/ --cov-fail-under=95 --cov-report=html"
                            }
                            publishHTML target: [
                                allowMissing: false,
                                alwaysLinkToLastBuild: false,
                                keepAll: true,
                                reportDir: 'htmlcov',
                                reportFiles: 'index.html',
                                reportName: 'PyTestCov'
                            ]
                        }
                    }
                }
            }
        }
        stage ("Run unit tests") {
            steps {
                script {
                    customImage.inside("-v $WORKSPACE:/app") {
                        sh "python3 -m pytest -m unittest -v --junitxml=results/unittests_results.xml"
                    }
                }
            }
        }
        stage("Run tests") {
            matrix {
                axes {
                    axis {
                        name 'TEST_GROUP'
                        values 'iso', 'grub', 'image', 'install'
                    }
                }
                stages {
                    stage("Test stage") {
                        steps {
                            script {
                                echo "Running ${TEST_GROUP}"
                                customImage.inside("-v $WORKSPACE:/app") {
                                    sh "python3 -m pytest -m ${FLAG} -k ${TEST_GROUP} -v --junitxml=results/${TEST_GROUP}_results.xml"
                                }
                            }
                        }
                    }
                }
            }
        }
        stage ("Staging") {
            parallel {
                stage ("Scan for skipped tests") {
                    when {
                        expression {
                            return env.BRANCH_NAME == 'release' || env.BRANCH_NAME == 'master'
                        }
                    }
                    steps {
                        script {
                            sh 'python3 automated_tests/tools/python/scan_for_skipped_tests.py'
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: "**/*.xml, htmlcov/*.html"
            junit "**/*.xml"
            cleanWs()
        }
    }
}

def getTestEnvValue() {
    String return_value = "smoke"
    if (params.containsKey("TEST_FLAG")) {
        return_value = "${TEST_FLAG}"
    }
    return return_value
}