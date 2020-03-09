FROM python:3.6.8

ENV APP_PATH /opt/apps

COPY requirements.txt $APP_PATH/
RUN pip install --no-cache-dir -r $APP_PATH/requirements.txt
RUN    apt-get update \
    && apt-get install openssl \
    && apt-get install ca-certificates
RUN pip install --no-cache-dir pyopenssl

WORKDIR $APP_PATH