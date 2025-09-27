pipeline {
    agent any

    environment {
        S3_BUCKET = "employee-app-artifacts"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/sathishkrishnan645-design/employee-management-webapp.git'
            }
        }

        stage('Build') {
            steps {
                sh 'echo "Building Employee Management Web App..."'
            }
        }

        stage('Package') {
            steps {
                sh 'zip -r employee-app.zip *'
            }
        }

        stage('Upload to S3') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'jenkins-s3-user']]) {
                    sh 'aws s3 cp employee-app.zip s3://employee-app-artifacts/ --region ap-southeast-1'
                }
            }
        }

        stage('Deploy to Singapore EC2') {
            steps {
                sshagent(['sg-ec2-ssh']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ec2-user@18.142.30.111 '
                            mkdir -p ~/employee-management-webapp &&
                            cd ~/employee-management-webapp &&
                            aws s3 cp s3://employee-app-artifacts/employee-app.zip . --region ap-southeast-1 &&
                            unzip -o employee-app.zip &&
                            nohup python3 app.py > app.log 2>&1 &
                        '
                    """
                }
            }
        }
    }
}

