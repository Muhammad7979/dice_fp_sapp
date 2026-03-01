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

# Pull the server Docker image
sudo docker pull muhammad0897979/dice_project_server_app:latest

# Run the server container on port 5000
sudo docker run -d -p 5000:5000 muhammad0897979/dice_project_server_app:latest