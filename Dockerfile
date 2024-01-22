#Delcare python version 3.11.7 (Bulleye)
FROM python:3.11.7-bullseye

#Declare variable for HOME_PATH and WORK_DIR
#ARG work_path="API_EG"
ENV env_work_path=$work_path

WORKDIR /API_EG

#Copy All file in project move to Docker image folder.
COPY Gitlab/api_eg /API_EG
RUN ls /API_EG
RUN pwd

#Run Bash script for apt-get update
RUN apt-get update
RUN apt-get install ca-certificates apt-transport-https libnss3
RUN apt-get nano

#Get the google chrome Browser for Linux Server
RUN wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN ls /API_EG
RUN apt install -f /API_EG/google-chrome-stable_current_amd64.deb -y

#Upgrade pip before installing the package in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /API_EG/requirements.txt
RUN ls /API_EG

EXPOSE 8000

ENV TZ="Asia/Bangkok"

ENTRYPOINT ["python","/API_EG/manage.py","runserver","0:8000"]

