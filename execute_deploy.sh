#!/bin/bash

# Stop the running container
docker stop mysite

# Remove the stopped container
docker rm mysite

# Delete current or existing image
docker rmi AWS_ACCT_NUM.dkr.ecr.us-east-1.amazonaws.com/mysite:latest

# Login to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin AWS_ACCT_NUM.dkr.ecr.us-east-1.amazonaws.com/

# Pull latest image of mysite
docker pull AWS_ACCT_NUM.dkr.ecr.us-east-1.amazonaws.com/mysite:latest

# Run the image
docker run -d -p 8000:8000 --name mysite AWS_ACCT_NUM.dkr.ecr.us-east-1.amazonaws.com/mysite:latest
