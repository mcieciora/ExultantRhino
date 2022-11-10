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
                sh 'ls'
            }
        }
    }
}