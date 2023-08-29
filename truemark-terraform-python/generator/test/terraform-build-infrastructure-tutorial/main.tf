terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 3.27"
    }
  }
}

provider "aws" {
  profile = "default"
  region = "us-west-1"
}

resource "aws_instance" "app_server" {
  ami = "ami-0577b787189839998"
  instance_type = "t2.micro"
  tags = {
    Name = "2ndDemo_Third_ExampleAppServerInstance"
  }
}


resource "aws_instance" "app_server_third" {
  ami = "ami-0577b787189839998"
  instance_type = "t2.micro"
  tags = {
    Name = "2ndDemo_Fourth_ExampleAppServerInstance"
  }
}

