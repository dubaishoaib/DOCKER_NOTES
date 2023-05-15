FROM ubuntu

RUN apt-get -y update
RUN apt-get -y install software-properties-common
RUN add-apt-repository --yes ppa:deadsnakes/ppa
RUN apt-get -y update
RUN apt-get -y install python3.10
RUN apt-get -y install pip
RUN pip install -q flask
RUN pip install -q flask-mysql

COPY app.py /opt/app.py

ENTRYPOINT FLASK_APP=/opt/app.py flask run --host=0.0.0.0
