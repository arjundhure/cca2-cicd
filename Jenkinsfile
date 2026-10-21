
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'arjun1254/studentai'
        DOCKER_CREDENTIALS = 'dockerhub-creds'
        KUBECONFIG = '/var/lib/jenkins/.kube/config'
        MINIKUBE_HOME = '/var/lib/jenkins'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/arjundhure/cca2-cicd.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$BUILD_NUMBER .'
                sh 'docker tag $DOCKER_IMAGE:$BUILD_NUMBER $DOCKER_IMAGE:latest'
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    docker run --rm \
                        -v "$WORKSPACE:/app" \
                        -w /app \
                        "$DOCKER_IMAGE:$BUILD_NUMBER" \
                        python -m pytest -v
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKER_CREDENTIALS}",
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login \
                            -u "$DOCKER_USER" --password-stdin
                        docker push "$DOCKER_IMAGE:$BUILD_NUMBER"
                        docker push "$DOCKER_IMAGE:latest"
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    sed "s|image: arjun1254/studentai:latest|image: $DOCKER_IMAGE:$BUILD_NUMBER|" \
                        k8s/deployment.yaml > /tmp/studentai-deployment.yaml

                    kubectl apply -f /tmp/studentai-deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl rollout status deployment/studentai --timeout=180s
                    kubectl get pods
                    kubectl get services
                '''
            }
        }
    }

    post {
        success {
            echo 'StudentAi CI/CD pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the Console Output for details.'
        }
    }
}

