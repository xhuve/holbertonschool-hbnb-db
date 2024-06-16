FROM alpine:latest

WORKDIR /app

COPY . .

RUN apk update && xargs -a requirements.txt apk add 

ENV PORT=5000

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]