pipeline {
    agent any

    environment {
        EC2_USER = 'ec2-user'
        EC2_HOST = '18.142.30.111' // Singapore EC2
        SSH_KEY = '/var/lib/jenkins/sg-ec2-key.pem'
        APP_ZIP = 'employee-app.zip'
        REMOTE_DIR = '/home/ec2-user/employee-app'
    }

    stages {
        stage('Upload to EC2') {
            steps {
                sshagent(credentials: ['ec2-user-ssh-key']) { // Jenkins credential ID
                    sh """
                        scp -i ${SSH_KEY} ${APP_ZIP} ${EC2_USER}@${EC2_HOST}:${REMOTE_DIR}/
                    """
                }
            }
        }

        stage('Deploy on EC2') {
            steps {
                sshagent(credentials: ['ec2-user-ssh-key']) {
                    sh """
                        ssh -i ${SSH_KEY} ${EC2_USER}@${EC2_HOST} 'unzip -o ${REMOTE_DIR}/${APP_ZIP} -d ${REMOTE_DIR} && echo Deployment complete'
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Application deployed successfully!"
        }
        failure {
            echo "Deployment failed. Check logs."
        }
    }
}

