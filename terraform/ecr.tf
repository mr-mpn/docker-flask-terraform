resource "aws_ecr_repository" "flask_app" {
  name                 = "flask-number-app"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project = "EightDigitApp"
  }
}
