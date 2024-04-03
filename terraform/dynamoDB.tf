resource "aws_dynamodb_table" "deltalake_locks" {
  name         = var.aws_dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "tablePath"
  range_key    = "fileName"

  attribute {
    name = "tablePath"
    type = "S"
  }

  attribute {
    name = "fileName"
    type = "S"
  }
}