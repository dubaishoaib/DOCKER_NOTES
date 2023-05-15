FROM ubuntu

RUN apt-get -y update
RUN apt-get -y install software-properties-common
RUN add-apt-repository --yes ppa:deadsnakes/ppa
RUN apt-get -y update
RUN apt-get -y install python3.10
RUN apt-get -y install pip
RUN pip install -q flask
RUN pip install -q flask-mysql

COPY app_color.py /opt/app_color.py

RUN export APP_COLOR=red

ENTRYPOINT FLASK_APP=/opt/app_color.py flask run --host=0.0.0.0
