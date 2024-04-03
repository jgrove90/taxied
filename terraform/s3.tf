resource "aws_s3_bucket" "bucket" {
  bucket        = var.s3_bucket_name
  force_destroy = true
}

resource "aws_s3_object" "bronze" {
  bucket        = aws_s3_bucket.bucket.bucket
  key           = "bronze/dummy"
  source        = "/dev/null"
  force_destroy = true
}

resource "aws_s3_object" "silver" {
  bucket        = aws_s3_bucket.bucket.bucket
  key           = "silver/dummy"
  source        = "/dev/null"
  force_destroy = true
}

resource "aws_s3_object" "gold" {
  bucket        = aws_s3_bucket.bucket.bucket
  key           = "gold/dummy"
  source        = "/dev/null"
  force_destroy = true
}