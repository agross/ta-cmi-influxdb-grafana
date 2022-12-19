FROM python:3-alpine

RUN apk add --no-cache \
            --update \
            curl \
            jq \
            \
    && \
    pip --no-cache-dir install pycryptodome

WORKDIR /app

COPY ./main .
COPY ./airq.py .

CMD ["./main"]
