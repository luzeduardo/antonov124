FROM gliderlabs/alpine:3.3
RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

WORKDIR /app
COPY . /app
RUN virtualenv /env && source /env/bin/activate && /env/bin/pip install -r /app/requirements.txt && pip install selenium

CMD ["/env/bin/python2", "google.py"]
