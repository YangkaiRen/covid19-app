#!/bin/bash

DIR="/home/ec2-user/covid19-app"
if [ -d "$DIR" ]; then
    echo "$DIR exists"
else
    echo "make dir $DIR"
    mkdir $DIR
fi