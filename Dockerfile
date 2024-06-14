FROM alpine:latest

RUN apk add python3 py3-pip py3-flask py3-email-validator

WORKDIR /app

COPY . .

RUN python3 -m venv venv && \
    source venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

ENV PORT=5000

EXPOSE 5000

CMD ["python3", "app.py"]