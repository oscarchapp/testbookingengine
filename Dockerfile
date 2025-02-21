# Using Python 3.11 for this test instead of "latest" because cgi was removed on Python 3.13 (PEP 594)
# Link to the offical docs of cgi library: https://docs.python.org/3/library/cgi.html
FROM python:3.11

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
