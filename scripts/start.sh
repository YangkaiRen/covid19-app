#!/bin/bash

cd /home/ec2-user/covid19-app
streamlit run app.py > app.log 2>&1 &