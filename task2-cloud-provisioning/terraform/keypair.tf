resource "tls_private_key" "d417_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "aws_key_pair" "d417_key" {
  key_name   = "d417-task2-key"
  public_key = tls_private_key.d417_key.public_key_openssh
}

resource "local_file" "d417_private_key" {
  content         = tls_private_key.d417_key.private_key_pem
  filename        = "${path.module}/d417-task2-key.pem"
  file_permission = "0400"
}
