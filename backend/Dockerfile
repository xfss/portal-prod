FROM python:3-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
 && apk add libc-dev linux-headers postgresql-dev make build-base gcc glib git pcre-dev libressl-dev curl nginx bash gettext \
            libffi-dev jpeg-dev zlib-dev openjpeg-dev tiff-dev pango-dev freetype-dev py-cffi cairo-dev ttf-freefont

ENV GOSU_VERSION 1.9

RUN curl -L -o /usr/local/bin/gosu \
    https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-amd64 \
 && chmod +x /usr/local/bin/gosu

ENV CONFD_VERSION 0.11.0

RUN curl -L -o /usr/local/bin/confd \
  https://github.com/kelseyhightower/confd/releases/download/v$CONFD_VERSION/confd-$CONFD_VERSION-linux-amd64 \
 && chmod +x /usr/local/bin/confd

ENV FOREGO_VERSION stable

RUN curl https://bin.equinox.io/c/ekMN3bCZFUn/forego-$FOREGO_VERSION-linux-amd64.tgz | tar xz -C /usr/local/bin \
 && chmod +x /usr/local/bin/forego

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

# ensure www-data user exists
# 82 is the standard uid/gid for "www-data" in Alpine
RUN set -x ; \
  addgroup -g 82 -S www-data ; \
  adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1

RUN mkdir /etc/uwsgi \
 && mkdir /run/uwsgi \
 && chown www-data:www-data /run/uwsgi

RUN mkdir /run/nginx \
 && chown -R www-data:www-data /run/nginx/

ADD . /code/

RUN chmod +x /code/start.sh

ENTRYPOINT ["/code/start.sh"]

CMD ["start"]

RUN chown -R www-data:www-data /code
