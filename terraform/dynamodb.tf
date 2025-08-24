resource "aws_dynamodb_table" "eight_digit" {
  name         = "EightDigit"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "username"
  range_key    = "timestamp"

  attribute {
    name = "username"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  tags = {
    Project = "EightDigitApp"
  }
}
