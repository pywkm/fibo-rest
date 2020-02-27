FROM python:3.7-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /app/src/

WORKDIR /app/src

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY ./src/ingest/requirements.txt ./
RUN pip install -r requirements.txt

COPY src ./src

ENTRYPOINT ["python", "ingest/main.py"]
