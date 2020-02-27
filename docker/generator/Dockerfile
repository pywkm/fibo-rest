FROM python:3.7-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /app/src/

WORKDIR /app/src

COPY ./src/generator/requirements.txt ./
RUN pip install -r requirements.txt

COPY src ./src

ENTRYPOINT ["python", "generator/main.py"]
