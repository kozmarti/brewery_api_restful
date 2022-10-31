# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# install dependencies  
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# port where the Django app runs  
EXPOSE 8000  

CMD python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py loaddata fixtures && python3 manage.py runserver 0.0.0.0:8000
