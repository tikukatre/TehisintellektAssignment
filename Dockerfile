FROM python:latest

RUN apt-get update && apt-get install -y git && apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY . .

CMD uvicorn app.main:app --host 0.0.0.0 --reload