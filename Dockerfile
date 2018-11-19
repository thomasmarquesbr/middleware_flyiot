FROM python:3
LABEL maintainer="Thomás Marques"
COPY . /usr/src/app
WORKDIR /usr/src/app
ENTRYPOINT ["python3", "start.py"]