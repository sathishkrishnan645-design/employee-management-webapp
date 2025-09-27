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
                s3Upload(bucket: "${S3_BUCKET}", 
                         stage('Upload to S3') {
    steps {
        s3Upload(
            bucket: "${S3_BUCKET}",
            includePathPattern: 'employee-app.zip',
            workingDir: '',
            path: '',
            acl: 'Private',
            region: 'ap-southeast-1'   // <- region inside parentheses
        )
    }
}

