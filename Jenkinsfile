pipeline {
    agent {
        docker {
            image 'python:3.9-slim'
            args '-u root'
        }
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/SamanBarahoie/security-header-checker.git', branch: 'main'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pytest -v'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}