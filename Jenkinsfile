pipeline {
    agent any

    environment {
        GIT_CREDENTIALS = 'github-credentials'
        S3_BUCKET = 'employee-app-artifacts'
        AWS_REGION = 'ap-southeast-1'
        EC2_KEY_PATH = '/var/lib/jenkins/sg-ec2-key.pem'
        EC2_USER = 'ec2-user'
        EC2_HOST = '18.142.30.111'
        APP_DIR = 'employee-management-webapp'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                git branch: 'main', url: 'https://github.com/sathishkrishnan645-design/employee-management-webapp.git', credentialsId: "${GIT_CREDENTIALS}"
            }
        }

        stage('Build') {
            steps {
                echo 'Building Employee Management Web App...'
                sh '''
                zip -r employee-app.zip Jenkinsfile README.md app.py
                '''
            }
        }

        stage('Upload to S3') {
            steps {
                withAWS(region: "${AWS_REGION}", credentials: 'aws-creds') {
                    s3Upload(bucket: "${S3_BUCKET}",
                             includePathPattern: 'employee-app.zip',
                             workingDir: '',
                             path: '',
                             acl: 'Private')
                }
            }
        }

        stage('Deploy to Singapore EC2') {
            steps {
                sh """
                ssh -i ${EC2_KEY_PATH} ${EC2_USER}@${EC2_HOST} << 'EOF'
                mkdir -p ~/${APP_DIR}
                cd ~/${APP_DIR}
                aws s3 cp s3://${S3_BUCKET}/employee-app.zip .
                unzip -o employee-app.zip
                nohup python3 app.py &
                EOF
                """
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs.'
        }
    }
}

