output "server_public_ip" {
  value = aws_instance.server.public_ip
}

output "client_public_ip" {
  value = aws_instance.client.public_ip
}
