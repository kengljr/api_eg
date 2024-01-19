FROM python:3.11.7-bullseye

ARG work_path="API_EG"
ENV env_work_path=$work_path
WORKDIR $work_path

COPY ${HOME}/api_eg $work_path

RUN apt-get update
RUN apt-get install ca-certificates apt-transport-https libnss3
RUN wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN ls $work_path
RUN apt install -f ${HOME}/google-chrome-stable_current_amd64.deb -y


RUN pip install --upgrade pip
RUN pip install -r ${HOME}/requirements.txt
RUN ls $work_path

EXPOSE 8000

ENV TZ="Asia/Bangkok"

ENTRYPOINT ["python",${HOME}/${env_work_path}/manage.py,"runserver","0:8000"]

