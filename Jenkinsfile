
pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Python Syntax Check') {
            steps {
                sh 'python3 -m py_compile app.py test_app.py'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t aceest-fitness:jenkins-build .'
            }
        }

        stage('Pytest in Docker') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$WORKSPACE:/results" \
                      --entrypoint /bin/sh \
                      aceest-fitness:jenkins-build \
                      -c "pip install pytest && \
                      cp /results/test_app.py /app/test_app.py && \
                      cd /app && \
                      python -m pytest -v \
                      --junitxml=/results/pytest-results.xml"
                '''
            }
        }

        stage('Container Health Check') {
            steps {
                sh '''
                    docker rm -f aceest-ci-test 2>/dev/null || true

                    docker run -d \
                      --name aceest-ci-test \
                      -p 127.0.0.1:8090:5000 \
                      aceest-fitness:jenkins-build

                    sleep 5

                    curl --fail http://127.0.0.1:8090/health
                    curl --fail http://127.0.0.1:8090/release
                '''
            }
        }


        stage('Publish Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-aceest',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {
                    sh '''
                        set +x
                        printf '%s' "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin

                        docker tag aceest-fitness:jenkins-build \
                          "$DOCKER_USER/aceest-fitness:ci-${BUILD_NUMBER}"

                        docker push "$DOCKER_USER/aceest-fitness:ci-${BUILD_NUMBER}"

                        docker logout
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'docker rm -f aceest-ci-test 2>/dev/null || true'
            junit allowEmptyResults: true, testResults: 'pytest-results.xml'
        }

        success {
            echo 'ACEest Fitness CI pipeline completed successfully'
        }

        failure {
            echo 'ACEest Fitness CI pipeline failed'
        }
    }
}


