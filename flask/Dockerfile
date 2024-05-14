FROM python:3.11-alpine

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 8000

ENV FLASK_APP=run.py
ENV FLASK_RUN_PORT 8000
ENV FLASK_RUN_HOST 0.0.0.0


CMD ["flask", "run"]
