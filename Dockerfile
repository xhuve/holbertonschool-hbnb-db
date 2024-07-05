FROM python:3-alpine

WORKDIR /app

COPY . .

RUN apk update && \
    apk add --no-cache mysql-dev mysql-client && \
    apk add --virtual build-deps gcc python3-dev musl-dev libffi-dev openssl-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apk del build-deps

ENV PORT=5000

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run_app:app"]