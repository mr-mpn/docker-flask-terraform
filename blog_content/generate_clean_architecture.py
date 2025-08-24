import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

# Colors
vpc_color = '#E8F4FD'
public_color = '#D4F1F4'
aws_service_color = '#FF9900'
container_color = '#4CAF50'
db_color = '#2196F3'
security_color = '#FFD93D'
logs_color = '#FF6B6B'

# Title
ax.text(8, 11.5, 'Flask Web Application Architecture on AWS', 
        fontsize=20, fontweight='bold', ha='center', color='#2C3E50')

# AWS Cloud boundary
cloud = FancyBboxPatch((0.5, 0.5), 15, 10.5, boxstyle="round,pad=0.1", 
                       facecolor='#F8F9FA', edgecolor='#4169E1', linewidth=2)
ax.add_patch(cloud)
ax.text(1, 10.8, 'AWS Cloud (eu-central-1)', fontsize=12, fontweight='bold', color='#4169E1')

# VPC
vpc = Rectangle((1, 1), 14, 9.5, facecolor=vpc_color, edgecolor='#1976D2', linewidth=2)
ax.add_patch(vpc)
ax.text(1.2, 10.2, 'VPC (10.0.0.0/16)', fontsize=14, fontweight='bold', color='#1976D2')

# Internet Gateway
igw = Rectangle((7.5, 9.8), 1, 0.6, facecolor=aws_service_color, edgecolor='black', linewidth=2)
ax.add_patch(igw)
ax.text(8, 10.1, 'IGW', fontsize=12, ha='center', fontweight='bold', color='black')

# Availability Zones
az1_box = Rectangle((1.5, 6.5), 6, 3.5, facecolor='#F5F5F5', edgecolor='#666', linewidth=2, linestyle='--')
ax.add_patch(az1_box)
ax.text(4.5, 9.7, 'Availability Zone eu-central-1a', fontsize=11, ha='center', fontweight='bold', color='#333')

az2_box = Rectangle((8.5, 6.5), 6, 3.5, facecolor='#F5F5F5', edgecolor='#666', linewidth=2, linestyle='--')
ax.add_patch(az2_box)
ax.text(11.5, 9.7, 'Availability Zone eu-central-1b', fontsize=11, ha='center', fontweight='bold', color='#333')

# Public Subnets (larger since no private subnets)
pub_subnet1 = Rectangle((2, 7), 5, 2.2, facecolor=public_color, edgecolor='#00796B', linewidth=2)
ax.add_patch(pub_subnet1)
ax.text(4.5, 8.7, 'Public Subnet 1 (10.0.1.0/24)', fontsize=12, ha='center', fontweight='bold', color='#00796B')


pub_subnet2 = Rectangle((9, 7), 5, 2.2, facecolor=public_color, edgecolor='#00796B', linewidth=2)
ax.add_patch(pub_subnet2)
ax.text(11.5, 8.7, 'Public Subnet 2 (10.0.2.0/24)', fontsize=12, ha='center', fontweight='bold', color='#00796B')


# ECS Tasks in Public Subnets
ecs_task1 = Rectangle((3, 7.3), 2.5, 1.2, facecolor=container_color, edgecolor='black', linewidth=2)
ax.add_patch(ecs_task1)
ax.text(4.25, 8.1, 'ECS Fargate Task', fontsize=10, ha='center', fontweight='bold', color='black')
ax.text(4.25, 7.8, 'Flask App :5000', fontsize=9, ha='center', color='black')

ecs_task2 = Rectangle((10, 7.3), 2.5, 1.2, facecolor=container_color, edgecolor='black', linewidth=2)
ax.add_patch(ecs_task2)
ax.text(11.25, 8.1, 'ECS Fargate Task', fontsize=10, ha='center', fontweight='bold', color='black')
ax.text(11.25, 7.8, 'Flask App :5000', fontsize=9, ha='center', color='black')

# ECS Cluster label
cluster_box = Rectangle((6.5, 6), 3, 0.8, facecolor='lightgreen', edgecolor='green', linewidth=2, alpha=0.8)
ax.add_patch(cluster_box)
ax.text(8, 6.4, 'ECS Fargate Cluster', fontsize=12, ha='center', fontweight='bold', color='darkgreen')
ax.text(8, 6.1, 'flask-cluster', fontsize=10, ha='center', color='darkgreen')

# AWS Services Row
# ECR Repository
ecr = Rectangle((1.5, 4.5), 2.5, 1.2, facecolor=aws_service_color, edgecolor='black', linewidth=2)
ax.add_patch(ecr)
ax.text(2.75, 5.4, 'ECR Repository', fontsize=11, ha='center', fontweight='bold', color='black')
ax.text(2.75, 5.1, 'flask-number-app', fontsize=9, ha='center', color='black')
ax.text(2.75, 4.8, 'Scan: Enabled', fontsize=8, ha='center', color='black')

# Security Groups
sg_box = Rectangle((4.5, 4.5), 2.5, 1.2, facecolor=security_color, edgecolor='black', linewidth=2)
ax.add_patch(sg_box)
ax.text(5.75, 5.4, 'Security Group', fontsize=11, ha='center', fontweight='bold', color='black')
ax.text(5.75, 5.1, 'Inbound: 5000', fontsize=9, ha='center', color='black')
ax.text(5.75, 4.8, 'Outbound: All', fontsize=8, ha='center', color='black')

# CloudWatch Logs
cloudwatch = Rectangle((7.5, 4.5), 2.5, 1.2, facecolor=logs_color, edgecolor='black', linewidth=2)
ax.add_patch(cloudwatch)
ax.text(8.75, 5.4, 'CloudWatch Logs', fontsize=11, ha='center', fontweight='bold', color='black')
ax.text(8.75, 5.1, '/ecs/flask-app', fontsize=9, ha='center', color='black')
ax.text(8.75, 4.8, 'Retention: 7d', fontsize=8, ha='center', color='black')

# IAM Roles
iam_box = Rectangle((10.5, 4.5), 2.5, 1.2, facecolor='#6BCF7F', edgecolor='black', linewidth=2)
ax.add_patch(iam_box)
ax.text(11.75, 5.4, 'IAM Roles', fontsize=11, ha='center', fontweight='bold', color='black')
ax.text(11.75, 5.1, 'Task Role', fontsize=9, ha='center', color='black')
ax.text(11.75, 4.8, 'Execution Role', fontsize=8, ha='center', color='black')

# Route Table
rt_box = Rectangle((2, 2.8), 2.5, 1, facecolor='lightblue', edgecolor='black', linewidth=2)
ax.add_patch(rt_box)
ax.text(3.25, 3.5, 'Public Route Table', fontsize=10, ha='center', fontweight='bold', color='black')
ax.text(3.25, 3.1, '0.0.0.0/0 → IGW', fontsize=8, ha='center', color='black')

# VPC Endpoint
vpc_endpoint = Circle((12.5, 3.2), 1.0 , facecolor='purple', edgecolor='black', linewidth=2)
ax.add_patch(vpc_endpoint)
ax.text(12.5, 3.4, 'VPC Endpoint', fontsize=10, ha='center', fontweight='bold', color='black')
ax.text(12.5, 3.1, 'DynamoDB', fontsize=10, ha='center', fontweight='bold', color='black')
# DynamoDB (outside VPC)
dynamo = Rectangle((13.5, 2), 2, 1.8, facecolor=db_color, edgecolor='black', linewidth=2)
ax.add_patch(dynamo)
ax.text(14.5, 3.2, 'DynamoDB', fontsize=12, ha='center', fontweight='bold', color='black')

# Internet symbol
ax.text(8, 11, 'Internet Users', fontsize=16, ha='center', fontweight='bold', color='#2C3E50')

# Arrows and connections
# Internet to IGW
ax.annotate('', xy=(8, 10.4), xytext=(8, 10.8), 
            arrowprops=dict(arrowstyle='->', lw=3, color='blue'))

# IGW to Public Subnets
ax.annotate('', xy=(4.5, 9.2), xytext=(7.8, 10.1), 
            arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
ax.annotate('', xy=(11.5, 9.2), xytext=(8.2, 10.1), 
            arrowprops=dict(arrowstyle='->', lw=2, color='blue'))

# ECS to ECR (image pull)
ax.annotate('', xy=(3.5, 5.7), xytext=(4, 7.3), 
            arrowprops=dict(arrowstyle='->', lw=2, color='green'))

# ECS to DynamoDB via VPC Endpoint
ax.annotate('', xy=(12.2, 3.5), xytext=(5.5, 7.8), 
            arrowprops=dict(arrowstyle='->', lw=2, color='purple'))

# ECS to CloudWatch
ax.annotate('', xy=(8.5, 5.7), xytext=(4.5, 7.5), 
            arrowprops=dict(arrowstyle='->', lw=2, color='red'))

# Data flow summary at bottom
flow_text = """Data Flow: User Request → IGW → Public Subnets → ECS Tasks → VPC Endpoint → DynamoDB
Architecture: Serverless Flask app with multi-AZ high availability and private database access"""

ax.text(8, 0.8, flow_text, fontsize=11, ha='center', color='#2C3E50', 
        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))

plt.tight_layout()
plt.savefig('flask_aws_architecture_clean.jpg', dpi=300, bbox_inches='tight', format='jpg', 
            facecolor='white', edgecolor='none')
plt.show()

print("Clean architecture diagram saved as 'flask_aws_architecture_clean.jpg'")