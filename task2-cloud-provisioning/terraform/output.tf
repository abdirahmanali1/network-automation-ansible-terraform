output "ubuntu_public_ip" {
  value = aws_instance.ubuntu_server.public_ip
}

output "rhel_public_ip" {
  value = aws_instance.rhel_server.public_ip
}
