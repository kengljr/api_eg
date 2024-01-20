FROM python:3.11.7-bullseye

RUN `USER_HOME=$(eval echo ~${SUDO_USER})`
RUN echo "export home_path=`echo ${USER_HOME}`" >> /envfile
RUN . /envfile; echo $home_path

ARG work_path="API_EG"
ENV env_work_path=$work_path
WORKDIR $work_path

COPY ${home_path}/api_eg $work_path

RUN apt-get update
RUN apt-get install ca-certificates apt-transport-https libnss3
RUN wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN ls $work_path
RUN apt install -f ${home_path}/google-chrome-stable_current_amd64.deb -y


RUN pip install --upgrade pip
RUN pip install -r ${home_path}/requirements.txt
RUN ls $work_path

EXPOSE 8000

ENV TZ="Asia/Bangkok"

ENTRYPOINT ["python",${home_path}/${env_work_path}/manage.py,"runserver","0:8000"]

