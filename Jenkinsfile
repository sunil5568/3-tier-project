pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: '2-Tier-project-V3',
                url: 'https://github.com/sunil5568/3-tier-project.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                export PYTHONPATH=.
                pytest test_app.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t task-manager:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-secret',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Images') {
            steps {
                sh '''
                docker tag task-manager:${BUILD_NUMBER} sunil2211/task-manager:${BUILD_NUMBER}
                docker push sunil2211/task-manager:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        success {
            echo "Build Successful"
        }
        failure {
            echo "Build Failed"
        }
    }
}
