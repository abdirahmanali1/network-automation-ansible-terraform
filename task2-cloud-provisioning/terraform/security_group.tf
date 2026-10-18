resource "aws_security_group" "d417_sg" {
  name        = "d417-task2-sg"
  description = "Allow SSH access for D417 Task 2 servers"
  vpc_id      = data.aws_vpc.lab.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
