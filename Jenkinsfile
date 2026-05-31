pipeline {
    agent any

    environment {
        DOCKER_REPO = "sunil2211"
        FRONTEND_IMAGE = "${DOCKER_REPO}/task-frontend"
        BACKEND_IMAGE = "${DOCKER_REPO}/task-backend"
        // Replace this with your actual target deployment server IP
        DEPLOYMENT_SERVER_IP = "172.31.31.225" 
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/sunil5568/3-tier-project.git'
            }
        }

        stage('Build Backend Image') {
            steps {
                sh 'docker build -t $BACKEND_IMAGE:latest ./backend'
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh 'docker build -t $FRONTEND_IMAGE:latest ./frontend'
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
                    docker push $BACKEND_IMAGE:latest
                    docker push $FRONTEND_IMAGE:latest
                '''
            }
        }

                stage('Deploy to Kind') {
            steps {
                sshagent(['deploy-server-key']) {
                    sh """
                        ssh ubuntu@${DEPLOYMENT_SERVER_IP} << 'EOF'
                        # Navigate to your project directory on the remote server
                        cd ~/3-tier-project
                        git pull origin main

                        # Check if the Kind cluster 'kind' already exists
                        if ! kind get clusters | grep -q "^kind\$"; then
                            echo "Kind cluster not found. Creating cluster using config file..."
                            # Assumes your kind-config.yaml file is inside the repository (e.g., in the root or k8s/)
                            kind create cluster --config k8s/kind-config.yaml
                        else
                            echo "Kind cluster is already running."
                        fi

                        # Pull the latest Docker images on the remote machine
                        docker pull ${BACKEND_IMAGE}:latest
                        docker pull ${FRONTEND_IMAGE}:latest

                        # Apply Kubernetes manifests
                        kubectl apply -f k8s/
                        kubectl rollout restart deployment/backend
                        kubectl rollout restart deployment/frontend
EOF
                    """
                }
            }
        }

    }

    post {
        success {
            echo 'Images pushed and deployed successfully'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}
