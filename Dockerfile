
FROM markadams/chromium-xvfb

RUN apt-get update && apt-get install -y \
    python python-pip curl unzip libgconf-2-4

RUN pip install pytest selenium virtualenv

ENV CHROMEDRIVER_VERSION 2.19

RUN curl -SLO "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" \
  && unzip "chromedriver_linux64.zip" -d /usr/local/bin \
  && rm "chromedriver_linux64.zip"

WORKDIR /app
CMD ["python", "google.py"]