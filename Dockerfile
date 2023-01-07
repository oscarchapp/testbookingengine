FROM python:latest

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE="chapp.settings"

RUN mkdir /code
WORKDIR /code

RUN pip install --upgrade pip

# Install requirements
ADD requirements.txt /code/
RUN pip install -r requirements.txt

# Install debugpy for python debugging in VS code
RUN pip install debugpy -t /tmp

ADD . /code/

# create unprivileged user
RUN adduser --disabled-password --gecos '' myuser
