FROM oif/python3
RUN apk upgrade --update && apk add --no-cache dos2unix && rm /var/cache/apk/*

MAINTAINER Screaming_Bunny

LABEL name="Orchestrator Core" \
vendor="OpenC2" \
license="BSD" \
version="2.0" \
description="This is the Orchestrator Core container"

# Add files to container
ADD requirements.txt /tmp/requirements.txt
ADD orc_server /opt/orc_server
ADD docker-entrypoint.sh /docker-entrypoint.sh

# Set environment vars
# DJANGO Settings
ENV DJANGO_SETTINGS_MODULE=orchestrator.settings \
    DJANGO_ENV="prod"

# Requirements install
# System packages
RUN addgroup -S django && \
adduser -S django -G django && \
apk add --no-cache --virtual .build-deps \
  git \
  gcc \
  libc-dev \
  libffi-dev \
  openssl-dev \
  python3-dev \
  linux-headers && \
apk add --no-cache mailcap && \
# python/pip packages
pip3 install --no-cache-dir -r /tmp/requirements.txt && \
#
# Collect Static Filesz
cd /opt/orc_server && \
python3 manage.py collectstatic --noinput && \
cd && \
#
# Mod Entrypoint Script
chmod +x /docker-entrypoint.sh && \
chmod +x /opt/orc_server/dev_start.sh && \
dos2unix /docker-entrypoint.sh && \
dos2unix /opt/orc_server/dev_start.sh && \
chown -R django:django /opt/orc_server && \
#
# Cleanup
apk del .build-deps && \
rm -rf /var/cache/apk/* *.tar.gz* /usr/src /root/.gnupg /tmp/*

# Set the user for future commands
USER django

# Ports
EXPOSE 8080/tcp

# Orchestrator Core Working Directory
WORKDIR /opt/orc_server

# entrypoint Command
ENTRYPOINT ["/docker-entrypoint.sh"]

# Startup Command
CMD ["gunicorn", "-c", "gunicorn.conf.py", "orchestrator.wsgi:application"]
