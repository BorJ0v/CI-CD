provider "aws" {
  region = "eu-north-1"
}

# 1. Dynamic Search for the latest Ubuntu 24.04 AMI
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical's Official AWS ID
}

# 2. Upload your Public Key
resource "aws_key_pair" "docask_auth" {
  key_name   = "docask-key"
  public_key = file("~/.ssh/docask_key.pub")
}

# 3. Create the Firewall (Security Group)
resource "aws_security_group" "docask_sg" {
  name        = "docask-sg"
  description = "Allow SSH, Web, and K8s Traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 6443
    to_port     = 6443
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

# 4. Create the Server (EC2)
resource "aws_instance" "docask_server" {
  # This now points to our dynamic search result
  ami           = data.aws_ami.ubuntu.id 
  instance_type = "t3.micro"             

  key_name               = aws_key_pair.docask_auth.key_name
  vpc_security_group_ids = [aws_security_group.docask_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              curl -sfL https://get.k3s.io | sh -
              EOF

  tags = { Name = "DocAsk-Server" }
}

output "server_ip" {
  value = aws_instance.docask_server.public_ip
}
