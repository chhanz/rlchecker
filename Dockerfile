from python:3.10-buster

LABEL maintainer="chhanz"

WORKDIR /usr/src/app

COPY . .
RUN apt-get update \
    && apt-get -y install libmariadb-dev \
    && apt-get clean \
    && pip install --no-cache-dir -U pip setuptools \
    && pip install --no-cache-dir -r requirements.txt

CMD [ "python", "rss.py" ]
