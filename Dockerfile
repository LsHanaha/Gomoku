FROM --platform=linux/amd64 python:3.10

LABEL "author"="Trishin"

RUN apt-get update
RUN mkdir ./gomoku

COPY requirements.txt ./gomoku/
WORKDIR /gomoku
RUN pip install -r requirements.txt

COPY /app /gomoku/app
COPY start.py /gomoku
RUN mkdir /gomoku/logs


RUN cd ./app/algo && pip install ./algo_module && cd ../..

EXPOSE 8888
