# Flask Web Application Architecture on AWS

## Current Architecture Overview

```
                                    🌐 Internet
                                        |
                              ┌─────────────────┐
                              │ Internet Gateway │
                              └─────────────────┘
                                        |
    ┌─────────────────────────────────────────────────────────────────────┐
    │                        VPC (10.0.0.0/16)                           │
    │                                                                     │
    │  ┌─────────────────────┐              ┌─────────────────────┐      │
    │  │   Availability      │              │   Availability      │      │
    │  │     Zone 1a         │              │     Zone 1b         │      │
    │  │                     │              │                     │      │
    │  │ ┌─────────────────┐ │              │ ┌─────────────────┐ │      │
    │  │ │ Public Subnet 1 │ │              │ │ Public Subnet 2 │ │      │
    │  │ │ 10.0.1.0/24     │ │              │ │ 10.0.2.0/24     │ │      │
    │  │ │                 │ │              │ │                 │ │      │
    │  │ │  ┌─────────────┐│ │              │ │┌─────────────┐  │ │      │
    │  │ │  │ ECS Task    ││ │              │ ││ ECS Task    │  │ │      │
    │  │ │  │ Flask App   ││ │              │ ││ Flask App   │  │ │      │
    │  │ │  │ Port: 5000  ││ │              │ ││ Port: 5000  │  │ │      │
    │  │ │  └─────────────┘│ │              │ │└─────────────┘  │ │      │
    │  │ └─────────────────┘ │              │ └─────────────────┘ │      │
    │  │                     │              │                     │      │
    │  │                     │              │                     │      │
    │  │   (No private      │              │   (No private      │      │
    │  │    subnets needed) │              │    subnets needed) │      │
    │  │                     │              │                     │      │
    │  └─────────────────────┘              └─────────────────────┘      │
    │                                                                     │
    │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │
    │  │ ECR Repository  │    │ CloudWatch Logs │    │ Security Groups │ │
    │  │ flask-app       │    │ /ecs/flask-app  │    │ Port 5000       │ │
    │  └─────────────────┘    └─────────────────┘    └─────────────────┘ │
    │                                                                     │
    │  ┌─────────────────┐                          ┌─────────────────┐  │
    │  │ Public Route    │                          │ Private Route   │  │
    │  │ Table           │                          │ Table           │  │
    │  │ 0.0.0.0/0 → IGW │                          │ (Local only)    │  │
    │  └─────────────────┘                          └─────────────────┘  │
    │                                                                     │
    │                              ┌─────────────────┐                   │
    │                              │ VPC Endpoint    │                   │
    │                              │ (DynamoDB)      │                   │
    │                              └─────────────────┘                   │
    └─────────────────────────────────────────────────────────────────────┘
                                        |
                              ┌─────────────────┐
                              │ DynamoDB Table  │
                              │ "EightDigit"    │
                              │ Hash: username  │
                              │ Range: timestamp│
                              └─────────────────┘

    ┌─────────────────┐
    │ IAM Roles       │
    │ • Task Role     │
    │ • Execution Role│
    └─────────────────┘
```

## Architecture Components

### 1. **Networking Layer**
- **VPC**: Isolated network environment (10.0.0.0/16)
- **Public Subnets**: 2 subnets across 2 AZs for high availability
  - 10.0.1.0/24 (AZ-1a) and 10.0.2.0/24 (AZ-1b)
  - ECS tasks deployed here with public IPs
- **No Private Subnets**: Simplified architecture - not needed for this use case
- **Internet Gateway**: Provides internet access to public subnets
- **Route Tables**: Separate routing for public and private subnets

### 2. **Compute Layer**
- **ECS Fargate Cluster**: Serverless container platform
- **ECS Tasks**: Run Flask application containers
  - Deployed across multiple AZs for high availability
  - Auto-scaling capable
  - No server management required

### 3. **Container Registry**
- **ECR Repository**: Stores Docker images of Flask application
- **Image Scanning**: Enabled for security vulnerabilities

### 4. **Database Layer**
- **DynamoDB Table**: NoSQL database for storing user data
  - Table name: "EightDigit"
  - Hash key: username (String)
  - Range key: timestamp (String)
  - Pay-per-request billing

### 5. **Security & Access**
- **Security Groups**: Network-level firewall
  - Allows inbound HTTP traffic on port 5000
  - Allows all outbound traffic
- **IAM Roles**:
  - **Task Role**: Allows ECS tasks to access DynamoDB
  - **Execution Role**: Allows ECS to pull images and send logs
- **VPC Endpoint**: Private connection to DynamoDB (no internet routing)

### 6. **Monitoring & Logging**
- **CloudWatch Log Group**: Centralized logging for ECS tasks
- **Log retention**: 7 days

## Data Flow

1. **User Request**: Internet → Internet Gateway → Public Subnet → ECS Task
2. **Container Deployment**: ECR → ECS Task (image pull)
3. **Database Access**: ECS Task → VPC Endpoint → DynamoDB (private)
4. **Logging**: ECS Task → CloudWatch Logs
5. **Response**: ECS Task → Public Subnet → Internet Gateway → User

## High Availability Features

- **Multi-AZ Deployment**: Resources spread across 2 availability zones
- **Auto Scaling**: ECS service can scale tasks based on demand
- **Managed Services**: DynamoDB, ECR, and CloudWatch are fully managed
- **Private Database Access**: DynamoDB accessed via VPC endpoint (no internet)

## Security Features

- **Network Isolation**: VPC provides isolated network environment
- **Least Privilege**: IAM roles with minimal required permissions
- **Private Database Access**: DynamoDB not accessible from internet
- **Container Security**: ECR image scanning enabled
- **Network Security**: Security groups control traffic flow