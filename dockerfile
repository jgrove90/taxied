FROM python:3.12.1

WORKDIR /app

ADD src /app/src
ADD tests /app/tests
ADD requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80