pipeline {
    agent any

    environment {
        FRONTEND_IMAGE = "task-frontend"
        BACKEND_IMAGE = "task-backend"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                url: 'https://github.com/sunil5568/3-tier-project.git'
            }
        }

        stage('Verify Files') {
            steps {
                sh '''
                echo "Project files:"
                ls -la
                '''
            }
        }

        stage('Build Backend Image') {
            steps {
                sh '''
                docker build -t $BACKEND_IMAGE ./backend
                '''
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh '''
                docker build -t $FRONTEND_IMAGE ./frontend
                '''
            }
        }

        stage('Verify Docker Images') {
            steps {
                sh '''
                docker images
                '''
            }
        }
    }

    post {
        success {
            echo 'Build completed successfully!'
        }

        failure {
            echo 'Build failed!'
        }
    }
}