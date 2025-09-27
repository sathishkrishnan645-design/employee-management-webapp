pipeline {
    agent any

    environment {
        APP_NAME = "employee-management-webapp"
        EC2_USER = "ec2-user"
        EC2_HOST = "18.142.30.111"
        SSH_CREDENTIALS_ID = "sg-ec2-key" // Your Jenkins SSH credential ID
        DEPLOY_DIR = "/home/ec2-user/${APP_NAME}"
        WORKSPACE_DIR = "${env.WORKSPACE}"
        ZIP_FILE = "${APP_NAME}.zip"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/sathishkrishnan645-design/employee-management-webapp.git'
            }
        }

        stage('Build') {
            steps {
                echo "Building application..."
                // Example for Node.js app:
                sh 'npm install'
                sh 'npm run build'
                
                // Example for Java app (uncomment if needed):
                // sh './gradlew build'
            }
        }

        stage('Package') {
            steps {
                echo "Zipping application..."
                sh "zip -r ${ZIP_FILE} *"
            }
        }

        stage('Upload to S3') {
            steps {
                withAWS(region: 'ap-southeast-1', credentials: 'aws-creds') {
                    s3Upload(
                        bucket: 'your-s3-bucket-name',
                        includePathPattern: "${ZIP_FILE}",
                        workingDir: "${WORKSPACE_DIR}",
                        path: '',
                        acl: 'Private'
                    )
                }
            }
        }

        stage('Deploy to Singapore EC2') {
            steps {
                sshagent([SSH_CREDENTIALS_ID]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                            mkdir -p ${DEPLOY_DIR} &&
                            unzip -o /home/${EC2_USER}/${ZIP_FILE} -d ${DEPLOY_DIR} &&
                            cd ${DEPLOY_DIR} &&
                            # Run any app start commands below
                            # Example: npm install && npm start
                        '
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Deployment completed successfully!"
        }
        failure {
            echo "Pipeline failed. Check logs!"
        }
    }
}

