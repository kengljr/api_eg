#Delcare python version 3.11.7 (Bulleye)
FROM python:3.11.7-bullseye

#Declare variable for HOME_PATH and WORK_DIR
ARG work_path="API_EG"
ARG user="kengljr"
#ENV HOME="/home/$user"
ENV env_work_path=$work_path
WORKDIR $work_path
RUN su - $user
RUN echo $HOME

#Check first THS directory Exists if not so Mkdir
RUN mkdir -p $HOME/ths

#Copy All file in project move to Docker image folder.
COPY ${home_path}/api_eg $HOME/ths/$work_path

#Run Bash script for apt-get update
RUN apt-get update
RUN apt-get install ca-certificates apt-transport-https libnss3

#Get the google chrome Browser for Linux Server
RUN wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN ls $work_path
RUN apt install -f ${home_path}/google-chrome-stable_current_amd64.deb -y

#Upgrade pip before installing the package in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r ${home_path}/requirements.txt
RUN ls $work_path

EXPOSE 8000

ENV TZ="Asia/Bangkok"

ENTRYPOINT ["python",${home_path}/${env_work_path}/manage.py,"runserver","0:8000"]

