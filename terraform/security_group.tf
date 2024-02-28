resource "aws_security_group" "main" {
  vpc_id = aws_vpc.main.id
}