#!/bin/bash
sudo yum -y update
sudo pip3 install pandas streamlit plotly PyMySQL requests sqlalchemy
sudo yum -y install ruby
cd /home/ec2-user
curl -O https://aws-codedeploy-us-east-2.s3.amazonaws.com/latest/install
sudo chmod +x ./install
sudo ./install auto