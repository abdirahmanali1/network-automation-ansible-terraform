
resource "aws_instance" "ubuntu_server" {
  ami                         = "ami-0c520e17e31a43675"
  instance_type               = "t2.micro"
  subnet_id                   = data.aws_subnets.lab.ids[0]
  key_name                    = aws_key_pair.d417_key.key_name
  vpc_security_group_ids      = [aws_security_group.d417_sg.id]
  associate_public_ip_address = true

  tags = {
    Name = "D417-Ubuntu-Server"
  }
  
  lifecycle {
    ignore_changes = [tags, tags_all]
  }
}
