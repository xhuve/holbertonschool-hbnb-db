FROM alpine:latest

WORKDIR /app

COPY . .

RUN apk update && xargs -a requirements.txt apk add 

ENV PORT=5000

EXPOSE 5000

CMD ["python3", "app.py"]