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
                // Uses Jenkins AWS credentials to upload via AWS CLI
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
                    sh 'aws s3 cp employee-app.zip s3://employee-app-artifacts/ --region ap-southeast-1'
                }
            }
        }
    }
}

