pipeline {
    agent any

    environment {
        EC2_USER = 'ec2-user'
        EC2_HOST = '18.142.30.111'
        SSH_KEY_PATH = '/var/lib/jenkins/sg-ec2-key.pem'
        S3_BUCKET = 'your-s3-bucket-name'
        APP_NAME = 'employee-app.zip'
        APP_DIR = '/home/ec2-user/employee-app'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/sathishkrishnan645-design/employee-management-webapp.git',
                    credentialsId: 'github-credentials',
                    branch: 'main'
            }
        }

        stage('Build App') {
            steps {
                echo 'Skipping build since employee-app.zip is already in S3'
                // If you need npm build, uncomment below:
                // sh 'npm install'
                // sh 'zip -r employee-app.zip .'
            }
        }

        stage('Deploy to Singapore EC2') {
            steps {
                sshagent(['ec2-user']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no -i ${SSH_KEY_PATH} ${EC2_USER}@${EC2_HOST} \\
                    'mkdir -p ${APP_DIR} && \\
                    aws s3 cp s3://${S3_BUCKET}/${APP_NAME} ${APP_DIR}/ && \\
                    unzip -o ${APP_DIR}/${APP_NAME} -d ${APP_DIR} && \\
                    pkill -f app.py || true && \\
                    nohup python3 ${APP_DIR}/app.py > ${APP_DIR}/app.log 2>&1 &'
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment succeeded!'
        }
        failure {
            echo 'Deployment failed. Check logs!'
        }
    }
}

