#!/bin/bash
# Update and upgrade packages
sudo apt update -y
sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io

# Enable and start Docker service
sudo systemctl enable docker
sudo systemctl start docker

# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu

# Set server IP dynamically via Terraform interpolation
SERVER_IP=${aws_instance.server.private_ip}

# Pull client Docker image
sudo docker pull muhammad0897979/dice_project_client_app:latest

# Run client container on port 5000 and pass SERVER_URL as env variable
# sudo docker run -d -p 5000:5000 -e SERVER_URL=http://10.0.1.131:5000/data muhammad0897979/dice_project_client_app:latest
sudo docker run -d -p 5000:5000 -e SERVER_URL=http://$SERVER_IP:5000/data muhammad0897979/dice_project_client_app:latest