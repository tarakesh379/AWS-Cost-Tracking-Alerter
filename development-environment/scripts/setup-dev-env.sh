#!/bin/bash

echo "Setting up CentOS Stream 9 AWS Development Environment..."
echo "This script will set up your system for AWS development"

echo "Updating system packages..."
sudo dnf update -y

echo "Installing development tools..."
sudo dnf groupinstall "Development Tools" -y
sudo dnf install -y python3 python3-pip python3-venv git vim nano tree wget curl unzip

echo "Setting hostname to centos-aws-dev..."
sudo hostnamectl set-hostname cenntos-aws-dev
echo "127.0.0.1 centos-aws-dev" | sudo tee -a /etc/hosts

echo "Installing AWS CLI v2..."
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" 
unzip awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip

echo "Configuring Git..."
git config --global user.name "tarakesh379"
git config --global user.email "tarakeswaranaidu379@gmail.com"

echo "Creating project directory..."
mkdir -p ~/projects/aws-cost-tracker
cd ~/projects/aws-cost-tracker

echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pipp
pip install boto3 awscli

echo "Verifying installations..."
echo "CentOS Version: $(cat /etc/centos-release)"
echo "Hostname: $(hostname)"
echo "Python: $(python3 --version)"
echo "Git: $(git --version)"

echo "CentOS Stream 9 development environment ready!"
echo "Location: ~/projects/aws-cost-tracker"
echo "Activate venv: source venv/bin/activate"
echo "Next: Configure AWS CLI with 'aws configure' "

