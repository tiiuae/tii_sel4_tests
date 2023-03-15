# syntax=docker/dockerfile:1
FROM python:3.8
WORKDIR /app

RUN apt update
RUN apt install -y apt-utils libsnappy-dev
RUN pip install --upgrade pip
RUN git clone https://github.com/labgrid-project/labgrid
RUN cd labgrid && pip install ".[crossbar]"

EXPOSE 20408
CMD ["crossbar", "start"]
