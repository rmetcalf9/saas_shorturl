FROM python:3.11-bookworm

# =========================
# Metadata
# =========================
LABEL maintainer="Robert Metcalf"

# =========================
# Environment
# =========================
ENV APP_DIR=/app
ENV APIAPP_FRONTEND=/frontend
ENV APIAPP_FRONTEND_FRONTEND=/frontend

ENV APIAPP_APIURL=http://localhost:80/api
ENV APIAPP_APIDOCSURL=http://localhost:80/apidocs
ENV APIAPP_FRONTENDURL=http://localhost:80/frontend
ENV APIAPP_APIACCESSSECURITY='[]'
ENV APIAPP_DEFAULTMASTERTENANTJWTCOLLECTIONALLOWEDORIGINFIELD="http://localhost"

#Port for python app should always be 80 as this is is hardcoded in nginx config
ENV APIAPP_PORT 80

# APIAPP_MODE is now defined here instead of run_app_docker.sh
#  this is to enable dev mode containers (and avoid dev cors errors)
ENV APIAPP_MODE DOCKER

# APIAPP_VERSION is not definable here as it is read from the VERSION file inside the image

EXPOSE 80


# =========================
# System deps (Debian-based, stable)
# =========================
RUN apt-get update && apt-get install -y \
    nginx \
    bash \
    curl \
    build-essential \
    libpcre3-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# =========================
# App structure
# =========================
RUN mkdir -p ${APP_DIR} \
    && mkdir -p ${APIAPP_FRONTEND_FRONTEND} \
    && mkdir -p /var/log/uwsgi

# =========================
# Python deps
# =========================
COPY ./services/src ${APP_DIR}

RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir uwsgi \
    && pip install --no-cache-dir -r ${APP_DIR}/requirements.txt

# =========================
# Static/config files
# =========================
COPY ./VERSION /VERSION
COPY ./services/run_app_docker.sh /run_app_docker.sh
COPY ./nginx_default.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi.ini /uwsgi.ini
COPY ./healthcheck.sh /healthcheck.sh

RUN chmod +x /run_app_docker.sh /healthcheck.sh

# =========================
# TLS bundle (if needed for AWS/RDS)
# =========================
RUN curl -o /rds-combined-ca-bundle.pem \
    https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem

# =========================
# Runtime
# =========================
STOPSIGNAL SIGTERM

CMD ["/run_app_docker.sh"]

# Regular checks. Docker won't send traffic to container until it is healthy
#  and when it first starts it won't check the health until the interval so I can't have
#  a higher value without increasing the startup time
HEALTHCHECK --interval=30s --timeout=3s \
  CMD /healthcheck.sh


## OLD BELOW
# baseapp forces us to create the frontend directory of app will not load
#RUN apk add --no-cache bash python3 curl python3-dev build-base linux-headers pcre-dev libffi-dev && \
#    python3 -m ensurepip && \
#    rm -r /usr/lib/python*/ensurepip && \
#    pip3 install --upgrade pip setuptools && \
#    rm -r /root/.cache && \
#    pip3 install --upgrade pip && \
#    mkdir ${APP_DIR} && \
#    mkdir ${APIAPP_FRONTEND_FRONTEND} && \
#    mkdir /var/log/uwsgi && \
#    pip3 install uwsgi && \
#    wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem -O /rds-combined-ca-bundle.pem
