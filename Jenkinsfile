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
        FORCE_DOCKER_IMAGE_BUILD = getValue("FORCE_BUILD", false)
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
                            sh "docker build --no-cache -t test_image -f automated_tests/Dockerfile ."
                            if (env.BRANCH_TO_USE == "master" || env.BRANCH_TO_USE == "develop") {
                                sh "docker tag test_image ${DOCKERHUB_REPO}:test_image"
                                sh "docker push ${DOCKERHUB_REPO}:test_image"
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
                            sh "docker pull ${DOCKERHUB_REPO}:test_image"
                            sh "docker tag ${DOCKERHUB_REPO}:test_image test_image"
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
                            sh "docker run --rm test_image python -m pylint src --max-line-length=120 --disable=C0114 --fail-under=8.5"
                            sh "docker run --rm test_image python -m pylint --load-plugins pylint_pytest automated_tests --max-line-length=120 --disable=C0114,C0116 --fail-under=9.5"
                            sh "docker run --rm test_image python -m pylint tools/python --max-line-length=120 --disable=C0114 --fail-under=9.5"
                        }
                    }
                }
                stage ("flake8") {
                    steps {
                        script {
                            sh "docker run --rm test_image python -m flake8 --max-line-length 120 --max-complexity 10 src automated_tests tools/python"
                        }
                    }
                }
                stage ("ruff") {
                    steps {
                        script {
                            sh "docker run --rm test_image python -m ruff check src automated_tests tools/python"
                        }
                    }
                }
                stage ("black") {
                    steps {
                        script {
                            sh "docker run --rm test_image python -m black src automated_tests tools/python"
                        }
                    }
                }
                stage ("bandit") {
                    steps {
                        script {
                            sh "docker run --rm test_image python -m bandit src automated_tests tools/python"
                        }
                    }
                }
                stage ("pydocstyle") {
                    steps {
                        script {
                            sh "docker run --rm test_image python -m pydocstyle --ignore D100,D104,D107,D203,D204,D212 ."
                        }
                    }
                }
                stage ("radon") {
                    steps {
                        script {
                            sh "docker run --rm test_image python -m radon cc ."
                            sh "docker run --rm test_image python -m radon mi ."
                            sh "docker run --rm test_image python -m radon hal ."
                        }
                    }
                }
                stage ("mypy") {
                    when {
                        expression {
                            return false
                        }
                    }
                    steps {
                        script {
                            sh "docker run --rm test_image python -m mypy src automated_tests tools/python"
                        }
                    }
                }
                stage ("Code coverage") {
                    steps {
                        script {
                            sh "docker run --name code_coverage_container test_image python -m pytest --cov=src automated_tests/unittest --cov-fail-under=70 --cov-config=automated_tests/.coveragerc --cov-report=html"
                        }
                    }
                    post {
                        always {
                            script {
                                try {
                                    sh "docker container cp code_coverage_container:/app/htmlcov ./"
                                } catch (Exception e) {
                                    echo "Failed to copy code coverage results."
                                }
                                sh "docker rm code_coverage_container"
                                archiveArtifacts artifacts: "htmlcov/*"
                            }
                        }
                    }
                }
                stage ("Scan for skipped tests") {
                    when {
                        expression {
                            return env.BRANCH_TO_USE.contains("release") || env.BRANCH_TO_USE == "master"
                        }
                    }
                    steps {
                        script {
                            sh "docker run --rm test_image python tools/python/scan_for_skipped_tests.py"
                        }
                    }
                }
            }
        }
        stage ("Run unit tests") {
            steps {
                script {
                    sh "docker run --name unit_test_container test_image python -m pytest -m unittest automated_tests -v --junitxml=results/unittests_results.xml"
                }
            }
            post {
                always {
                    script {
                        try {
                            sh "docker container cp unit_test_container:/app/results ./"
                        } catch (Exception e) {
                            echo "Failed to copy unit tests results."
                        }
                        sh "docker rm unit_test_container"
                        archiveArtifacts artifacts: "**/unittests_results.xml"
                    }
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
        stage ("Run tests [postgres]") {
            when {
                expression {
                    return env.TEST_GROUPS == "all" || env.TEST_GROUPS.contains("postgres")
                }
            }
            steps {
                script {
                    echo "Running postgres"
                    withCredentials([file(credentialsId: 'dot_env', variable: 'env_file')]) {
                        sh "docker run --network general_network --env-file ${env_file} --privileged --name postgres_test test_image python -m pytest -m ${FLAG} -k postgres automated_tests -v --junitxml=results/postgres_results.xml"
                    }
                }
            }
            post {
                always {
                    script {
                        try {
                            sh "docker container cp postgres_test:/app/results ./"
                        } catch (Exception e) {
                            echo "Failed to copy postgres results."
                        }
                        sh "docker rm postgres_test"
                        archiveArtifacts artifacts: "**/postgres_results.xml"
                    }
                }
            }
        }
        stage ("Run tests [streamlit]") {
            when {
                expression {
                    return env.TEST_GROUPS == "all" || env.TEST_GROUPS.contains("streamlit")
                }
            }
            steps {
                script {
                    echo "Running streamlit"
                    withCredentials([file(credentialsId: 'dot_env', variable: 'env_file')]) {
                        sh "docker run --network general_network --env-file ${env_file} --privileged --name streamlit_test test_image python -m pytest -m ${FLAG} -k streamlit automated_tests -v --junitxml=results/streamlit_results.xml"
                        if (env.BRANCH_TO_USE.contains("release") || env.BRANCH_TO_USE == "master") {
                            sh "docker run --network general_network --env-file ${env_file} --privileged --name streamlit_test test_image python -m pytest -m regression -k streamlit automated_tests -v --junitxml=results/streamlit_results.xml"
                        }
                    }
                }
            }
            post {
                always {
                    script {
                        try {
                            sh "docker container cp streamlit_test:/app/results ./"
                        } catch (Exception e) {
                            echo "Failed to copy streamlit results."
                        }
                        sh "docker rm streamlit_test"
                        archiveArtifacts artifacts: "**/streamlit_results.xml"
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
                                sh "docker build --no-cache -t custom_image -f app.Dockerfile ."
                                sh "docker tag custom_image ${DOCKERHUB_REPO}:${env.BRANCH_TO_USE}-${curDate}"
                                sh "docker push ${DOCKERHUB_REPO}:${env.BRANCH_TO_USE}-${curDate}"
                                if (env.BRANCH_TO_USE == "master") {
                                    sh "docker tag custom_image ${DOCKERHUB_REPO}:latest"
                                    sh "docker push ${DOCKERHUB_REPO}:latest"
                                }
                            }
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
            sh "docker compose down --rmi all -v"
            junit allowEmptyResults: true, testResults: "**/**_results.xml"
            publishHTML target: [
                allowMissing: false,
                alwaysLinkToLastBuild: false,
                keepAll: true,
                reportDir: "htmlcov",
                reportFiles: "index.html",
                reportName: "PyTestCov"
            ]
            cleanWs()
            sh "docker rmi test_image"
        }
    }
}


def getValue(variable, defaultValue) {
    return params.containsKey(variable) ? params.get(variable) : defaultValue
}
