FROM python:3.7-alpine

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/src

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY ./src/api/requirements.txt ./
RUN pip install -r requirements.txt

COPY src ./src
COPY ./docker/api/start.sh /scripts/start.sh

ENTRYPOINT ["/scripts/start.sh"]
