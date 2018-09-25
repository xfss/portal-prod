FROM node:9-alpine

RUN apk add --update --no-cache \
  nginx \
  bash \
  curl \
  gettext

ENV CONFD_VERSION 0.11.0

RUN curl -L -o /usr/local/bin/confd \
  https://github.com/kelseyhightower/confd/releases/download/v$CONFD_VERSION/confd-$CONFD_VERSION-linux-amd64 \
 && chmod +x /usr/local/bin/confd

WORKDIR /code

COPY package.json /code/package.json

COPY package-lock.json /code/package-lock.json

COPY semantic.json /code/semantic.json

RUN npm install

RUN npm install -g gulp xgettext-template gettext-vue easygettext

COPY . /code

# Build semantic ui dist files
RUN cd /code/src/vendors/semantic && gulp build

ARG ENV_FILE

COPY $ENV_FILE $ENV_FILE

RUN export $(cat $ENV_FILE | xargs) \
 && /code/maketranslations \
 && npm run build

# ensure www-data user exists
# 82 is the standard uid/gid for "www-data" in Alpine
RUN set -x ; \
  addgroup -g 82 -S www-data ; \
  adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1

RUN mkdir -p /run/nginx

RUN chmod +x /code/start.sh

ENTRYPOINT ["/code/start.sh"]

CMD ["start"]
