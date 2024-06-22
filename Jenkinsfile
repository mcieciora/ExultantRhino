def testImage
def curDate = new Date().format("yyMMdd-HHmm", TimeZone.getTimeZone("UTC"))
Integer build_test_image

pipeline {
    agent any
    environment {
        FLAG = getValue("FLAG", "smoke")
        TEST_GROUPS = getValue("TEST_GROUP", "all")
        REGULAR_BUILD = getValue("REGULAR_BUILD", true)
        BRANCH_TO_USE = getValue("BRANCH", env.BRANCH_NAME)
        REPO_URL = "git@github.com:mcieciora/ExultantRhino.git"
        DOCKERHUB_REPO = "mcieciora/exultant_rhino"
        FORCE_DOCKER_IMAGE_BUILD = getValue("FORCE_BUILD", true)
    }
    options {
        skipDefaultCheckout()
    }
    stages {
        stage ("Checkout branch") {
            steps {
                script {
                    def BRANCH_REV = env.BRANCH_TO_USE.equals("develop") || env.BRANCH_TO_USE.equals("master") ? "HEAD^1" : "origin/develop"
                    withCredentials([sshUserPrivateKey(credentialsId: "github_id", keyFileVariable: 'key')]) {
                        sh 'GIT_SSH_COMMAND="ssh -i $key"'
                        checkout scmGit(branches: [[name: "*/${BRANCH_TO_USE}"]], extensions: [], userRemoteConfigs: [[url: "${env.REPO_URL}"]])
                    }
                    withCredentials([file(credentialsId: 'dot_env', variable: 'env_file')]) {
                        sh 'cp $env_file .env'
                    }
                    currentBuild.description = "Branch: ${env.BRANCH_TO_USE}\nFlag: ${env.FLAG}\nGroups: ${env.TEST_GROUPS}"
                    build_test_image = sh(script: "git diff --name-only \$(git rev-parse HEAD) \$(git rev-parse ${BRANCH_REV}) | grep -e automated_tests -e src -e requirements",
                                          returnStatus: true)
                }
            }
        }
        stage ("Prepare docker images") {
            parallel {
                stage ("Build test image") {
                    when {
                        anyOf {
                            expression {build_test_image == 0}
                            expression {env.FORCE_DOCKER_IMAGE_BUILD.toBoolean() == true}
                        }
                    }
                    steps {
                        script {
                            testImage = docker.build("${DOCKERHUB_REPO}:test_image", "-f automated_tests/Dockerfile .")
                            if (env.BRANCH_TO_USE == "master" || env.BRANCH_TO_USE == "develop") {
                                docker.withRegistry("", "dockerhub_id") {
                                    testImage.push()
                                }
                            }
                        }
                    }
                }
                stage ("Pull test image") {
                    when {
                        allOf {
                            expression {build_test_image == 1}
                            expression {env.FORCE_DOCKER_IMAGE_BUILD.toBoolean() == false}
                        }
                    }
                    steps {
                        script {
                            testImage = docker.image("${DOCKERHUB_REPO}:test_image")
                        }
                    }
                }

                stage ("Build docker compose") {
                    steps {
                        script {
                            sh "docker compose build --no-cache"
                        }
                    }
                }
            }
        }
        stage ("Code analysis") {
            when {
                expression {
                    return env.REGULAR_BUILD == "true"
                }
            }
            parallel {
                stage ("pylint") {
                    steps {
                        script {
                            testImage.inside("--rm -v $WORKSPACE:/app") {
                                sh "python -m pylint src --max-line-length=120 --disable=C0114 --fail-under=8.5"
                                sh "python -m pylint --load-plugins pylint_pytest automated_tests --max-line-length=120 --disable=C0114,C0116 --fail-under=9.5"
                                sh "python -m pylint tools/python --max-line-length=120 --disable=C0114 --fail-under=9.5"
                            }
                        }
                    }
                }
                stage ("flake8") {
                    steps {
                        script {
                            testImage.inside("--rm -v $WORKSPACE:/app") {
                                sh "python -m flake8 --max-line-length 120 --max-complexity 10 src automated_tests tools/python"
                            }
                        }
                    }
                }
                stage ("ruff") {
                    steps {
                        script {
                            testImage.inside("--rm -v $WORKSPACE:/app") {
                                sh "python -m ruff check src automated_tests tools/python"
                            }
                        }
                    }
                }
                stage ("black") {
                    steps {
                        script {
                            testImage.inside("--rm -v $WORKSPACE:/app") {
                                sh "python -m black src automated_tests tools/python"
                            }
                        }
                    }
                }
                stage ("bandit") {
                    steps {
                        script {
                            testImage.inside("--rm -v $WORKSPACE:/app") {
                                sh "python -m bandit src automated_tests tools/python"
                            }
                        }
                    }
                }
                stage ("pydocstyle") {
                    steps {
                        script {
                            testImage.inside("--rm -v $WORKSPACE:/app") {
                                sh "python -m pydocstyle --ignore D100,D104,D107,D203,D212 ."
                            }
                        }
                    }
                }
                stage ("radon") {
                    steps {
                        script {
                            testImage.inside("--rm -v $WORKSPACE:/app") {
                                sh "python -m radon cc ."
                                sh "python -m radon mi ."
                                sh "python -m radon hal ."
                            }
                        }
                    }
                }
                stage ("mypy") {
                    steps {
                        script {
                            testImage.inside("--rm -v $WORKSPACE:/app") {
                                sh "python -m mypy src automated_tests tools/python"
                            }
                        }
                    }
                }
                stage ("Code coverage") {
                    steps {
                        script {
                            testImage.inside("--rm -v $WORKSPACE:/app") {
                                sh "python -m pytest --cov=src automated_tests/unittest --cov-fail-under=70 --cov-config=automated_tests/.coveragerc --cov-report=html"
                            }
                            publishHTML target: [
                                allowMissing: false,
                                alwaysLinkToLastBuild: false,
                                keepAll: true,
                                reportDir: "htmlcov",
                                reportFiles: "index.html",
                                reportName: "PyTestCov"
                            ]
                        }
                    }
                }
                stage ("Scan for skipped tests") {
                    when {
                        expression {
                            return env.BRANCH_TO_USE == "release" || env.BRANCH_TO_USE == "master"
                        }
                    }
                    steps {
                        script {
                            testImage.inside("--rm -v $WORKSPACE:/app") {
                                sh "python tools/python/scan_for_skipped_tests.py"
                            }
                        }
                    }
                }
            }
        }
        stage ("Run unit tests") {
            steps {
                script {
                    testImage.inside("--rm -v $WORKSPACE:/app") {
                        sh "python -m pytest -m unittest automated_tests -v --junitxml=results/unittests_results.xml"
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: "**/*_results.xml"
                    junit "**/*_results.xml"
                }
            }
        }
        stage ("Run app & health check") {
            steps {
                script {
                    sh "chmod +x tools/shell_scripts/app_health_check.sh"
                    sh "tools/shell_scripts/app_health_check.sh 30 1"
                }
            }
            post {
                failure {
                    sh "docker compose down --rmi all -v"
                }
            }
        }
        stage ("Run tests") {
            matrix {
                axes {
                    axis {
                        name "TEST_GROUP"
                        values "postgres"
                    }
                }
                stages {
                    stage ("Test stage") {
                        steps {
                            script {
                                executeTestGroup("${TEST_GROUP}", testImage)
                            }
                        }
                        post {
                            always {
                                archiveArtifacts artifacts: "**/*_results.xml"
                                junit "**/*_results.xml"
                            }
                        }
                    }
                }
            }
        }
        stage ("Staging") {
            when {
                expression {
                    return env.REGULAR_BUILD == "true"
                }
            }
            parallel {
                stage ("Push docker image") {
                    when {
                        expression {
                            return env.BRANCH_TO_USE == "master" || env.BRANCH_TO_USE == "develop"
                        }
                    }
                    steps {
                        script {
                            docker.withRegistry("", "dockerhub_id") {
                                def customImage = docker.build("${DOCKERHUB_REPO}:${env.BRANCH_TO_USE}-${curDate}")
                                customImage.push()
                                if (env.BRANCH_TO_USE == "master") {
                                    customImage.push("latest")
                                }
                            }
                            sh "docker rmi ${DOCKERHUB_REPO}:${env.BRANCH_TO_USE}-${curDate}"
                        }
                    }
                }
                stage ("Push tag") {
                    when {
                        expression {
                            return env.BRANCH_TO_USE == "master"
                        }
                    }
                    steps {
                        script {
                            def TAG_NAME = "${env.BRANCH_TO_USE}-${curDate}"
                            withCredentials([sshUserPrivateKey(credentialsId: "github_id", keyFileVariable: 'key')]) {
                                sh 'GIT_SSH_COMMAND="ssh -i $key"'
                                sh "git tag -a $TAG_NAME -m $TAG_NAME && git push origin $TAG_NAME"
                            }
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs()
            sh "docker rmi ${DOCKERHUB_REPO}:test_image"
            sh "docker compose down --rmi all -v"
        }
    }
}


def getValue(variable, defaultValue) {
    return params.containsKey(variable) ? params.get(variable) : defaultValue
}


def executeTestGroup(testGroup, testImage) {
    if (env.TEST_GROUPS == "all" || env.TEST_GROUPS.contains(testGroup)) {
        echo "Running ${testGroup}"
            withCredentials([file(credentialsId: 'dot_env', variable: 'env_file')]) {
                testImage.inside("--rm --network general_network --env-file ${env_file} -v $WORKSPACE:/app") {
                    sh "python -m pytest -m ${FLAG} -k ${testGroup} automated_tests -v --junitxml=results/${testGroup}_results.xml"
            }
        }
    }
    else {
        echo "Skipping execution."
    }
}