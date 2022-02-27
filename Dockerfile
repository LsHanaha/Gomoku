FROM python:3.9

LABEL "author"="Trishin"

RUN apt-get update
RUN mkdir ./shurl

RUN pip install pipenv
COPY Pipfile Pipfile.lock ./shurl/
WORKDIR /shurl
RUN pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r requirements.txt

COPY /app /shurl/app
COPY start.py /shurl
RUN mkdir /shurl/logs

EXPOSE 8888

#CMD [ "python3", "app.py" ]