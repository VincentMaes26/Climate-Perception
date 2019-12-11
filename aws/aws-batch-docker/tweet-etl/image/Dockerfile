FROM python:3.6

RUN apt-get update
RUN apt-get install -y unzip

ADD requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir app

COPY entrypoint.sh .

ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]
