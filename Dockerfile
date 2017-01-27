FROM gliderlabs/alpine:3.3
ENV PHANTOMBIN=phantomjs
ENV PHANTOMJS=phantomjs-2.1.1-linux-i686.tar.bz2
ENV PHANTOMJSVERSION=${PHANTOMJS}.tar.bz2
ENV PHANTOMJSURL=https://bitbucket.org/ariya/phantomjs/downloads/${PHANTOMJSVERSION}
RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

WORKDIR /app
COPY . /app
RUN virtualenv /env && source /env/bin/activate && /env/bin/pip install -r /app/requirements.txt && pip install -U selenium

CMD ["/env/bin/python2", "google.py"]
