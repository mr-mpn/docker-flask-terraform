# CloudWatch Log Group for ECS tasks
resource "aws_cloudwatch_log_group" "flask_logs" {
  name              = "/ecs/flask-app"
  retention_in_days = 7
  
  tags = {
    Project = "EightDigitApp"
  }
}