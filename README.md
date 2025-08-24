# Flask 8-Digit Number App on AWS

A complete serverless web application built with Flask and deployed on AWS using Terraform. Users can submit their username and an 8-digit number, with all data stored in DynamoDB and the latest entry displayed on the homepage.

## 🏗️ Architecture Overview

```
Internet → AWS Internet Gateway → VPC Public Subnets → ECS Fargate Tasks
                                                            ↓
                                                    VPC Endpoint
                                                            ↓
                                                      DynamoDB
```

### Components
- **Frontend**: Flask web application with responsive HTML interface
- **Backend**: Python Flask API with DynamoDB integration
- **Infrastructure**: AWS ECS Fargate, VPC, DynamoDB, ECR
- **Deployment**: Terraform Infrastructure as Code
- **Container**: Docker containerized application

## 🚀 Features

- ✅ **Responsive Web Interface**: Clean, mobile-friendly design
- ✅ **Real-time Data**: Displays the latest submitted entry
- ✅ **Input Validation**: Ensures exactly 8 digits are entered
- ✅ **Serverless Architecture**: No server management required
- ✅ **High Availability**: Multi-AZ deployment across 2 availability zones
- ✅ **Secure**: IAM-based authentication, VPC isolation
- ✅ **Cost Optimized**: Pay-per-use pricing model

## 📋 Prerequisites

### Required Tools
- **AWS CLI** (configured with credentials)
- **Terraform** (>= 1.3.0)
- **Docker** (for building container images)
- **Git** (for version control)

### AWS Account Requirements
- Active AWS account with billing enabled
- IAM user with the following permissions:
  - `AmazonEC2FullAccess`
  - `AmazonECSFullAccess`
  - `AmazonDynamoDBFullAccess`
  - `AmazonVPCFullAccess`
  - `IAMFullAccess`
  - `AmazonElasticContainerRegistryFullAccess`
  - `CloudWatchLogsFullAccess`

## 🛠️ Installation & Deployment

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd flask-8digit-aws
```

### Step 2: Configure AWS CLI
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region: eu-central-1
# Default output format: json
```

### Step 3: Deploy Infrastructure
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

**Note the ECR repository URL from the output - you'll need it for the next step.**

### Step 4: Build and Push Docker Image
```bash
# Navigate back to project root
cd ..

# Get ECR repository URL
ECR_URI=$(cd terraform && terraform output -raw ecr_repository_url)

# Authenticate Docker with ECR
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin $ECR_URI

# Build Docker image
docker build -t flask-number-app .

# Tag for ECR
docker tag flask-number-app:latest $ECR_URI:latest

# Push to ECR
docker push $ECR_URI:latest
```

### Step 5: Deploy Application
```bash
# Force ECS to pull the new image
aws ecs update-service --cluster flask-cluster --service flask-service --force-new-deployment --region eu-central-1
```

### Step 6: Get Application URL
```bash
# Get the public IP of your running task
echo "http://$(aws ecs describe-tasks --cluster flask-cluster --tasks $(aws ecs list-tasks --cluster flask-cluster --service-name flask-service --region eu-central-1 --query 'taskArns[0]' --output text) --region eu-central-1 --query 'tasks[0].attachments[0].details[?name==`publicIPv4Address`].value' --output text):5000"
```

## 📁 Project Structure

```
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── templates/
│   └── index.html        # Web interface
├── terraform/
│   ├── main.tf           # Provider configuration
│   ├── variables.tf      # Input variables
│   ├── vpc.tf           # VPC and networking
│   ├── security.tf      # Security groups
│   ├── iam.tf           # IAM roles and policies
│   ├── dynamodb.tf      # DynamoDB table
│   ├── ecr.tf           # Container registry
│   ├── ecs.tf           # ECS cluster and service
│   ├── endpoints.tf     # VPC endpoints
│   ├── cloudwatch.tf   # Logging configuration
│   ├── outputs.tf       # Output values
│   └── .gitignore       # Terraform ignore file
├── ARCHITECTURE.md       # Detailed architecture documentation
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables
The application uses these environment variables (automatically set by ECS):
- `DYNAMO_TABLE`: DynamoDB table name (default: "EightDigit")
- `AWS_REGION`: AWS region (default: "eu-central-1")

### Terraform Variables
Key variables in `terraform/variables.tf`:
- `aws_region`: AWS deployment region
- `vpc_cidr`: VPC CIDR block
- `public_subnets`: Public subnet CIDR blocks

## 🎯 Expected Results

### Successful Deployment
After successful deployment, you should have:
1. **Web Application**: Accessible via `http://<PUBLIC_IP>:5000`
2. **DynamoDB Table**: "EightDigit" table with username/timestamp keys
3. **ECS Service**: Running 1 task across 2 availability zones
4. **ECR Repository**: Contains your Flask application Docker image

### Application Functionality
- **Homepage**: Displays the latest submitted entry
- **Form Submission**: Users can enter username + 8 digits
- **Data Persistence**: All entries stored in DynamoDB
- **Real-time Updates**: Page refreshes show latest data

## 💰 Cost Estimation

**Monthly costs for light usage:**
- **ECS Fargate**: ~$15-30 (1 task running 24/7)
- **DynamoDB**: ~$1-5 (pay-per-request)
- **VPC**: Free
- **CloudWatch Logs**: ~$0.50-2
- **ECR**: ~$0.10 (storage)

**Total estimated monthly cost: $16-37**

## 🔒 Security Features

- **Network Isolation**: VPC with public/private subnet separation
- **IAM Authentication**: No hardcoded credentials
- **Least Privilege**: Minimal required permissions
- **Private Database Access**: DynamoDB accessed via VPC endpoint
- **Container Security**: ECR image scanning enabled
- **Encrypted Storage**: DynamoDB encryption at rest

## 🚨 Troubleshooting

### Common Issues

#### No Public IP Found
```bash
# Check service status
aws ecs describe-services --cluster flask-cluster --services flask-service --region eu-central-1

# Check for stopped tasks
aws ecs list-tasks --cluster flask-cluster --desired-status STOPPED --region eu-central-1

# Force new deployment
aws ecs update-service --cluster flask-cluster --service flask-service --force-new-deployment --region eu-central-1
```

#### ECR Authentication Issues
```bash
# Re-authenticate with ECR
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin <ECR_URI>
```

#### Task Startup Failures
```bash
# Check service events
aws ecs describe-services --cluster flask-cluster --services flask-service --region eu-central-1 --query 'services[0].events[0:3]'

# Check CloudWatch logs
aws logs describe-log-streams --log-group-name /ecs/flask-app --region eu-central-1
```

### Debug Commands
```bash
# Complete infrastructure status
cd terraform
terraform show

# ECS service health
aws ecs describe-services --cluster flask-cluster --services flask-service --region eu-central-1

# DynamoDB table status
aws dynamodb describe-table --table-name EightDigit --region eu-central-1
```

## 🧹 Cleanup

To avoid ongoing charges, destroy all resources:

```bash
# Delete ECR images first (if needed)
aws ecr delete-repository --repository-name flask-number-app --region eu-central-1 --force

# Destroy infrastructure
cd terraform
terraform destroy
```

**⚠️ Warning**: This will permanently delete all data and resources.

## 🔄 Development Workflow

### Making Changes
1. **Update Code**: Modify `app.py` or templates
2. **Rebuild Image**: `docker build -t flask-number-app .`
3. **Push to ECR**: Tag and push new image
4. **Deploy**: Force ECS service update

### Infrastructure Changes
1. **Modify Terraform**: Update `.tf` files
2. **Plan Changes**: `terraform plan`
3. **Apply Changes**: `terraform apply`

## 📚 Learning Resources

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

For issues and questions:
1. Check the troubleshooting section
2. Review AWS CloudWatch logs
3. Open an issue in this repository

---

**Built with ❤️ using AWS, Terraform, and Flask**