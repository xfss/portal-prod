#!/bin/ash

SEMANTIC_DIR="/code/src/vendors/semantic"

if [ "$1" = 'start' ]; then
  confd -onetime -backend env -confdir='/code/confd'
  /code/maketranslations
  if [ "$ENVIRONMENT" = 'local' ]; then
    cd $SEMANTIC_DIR
    if [ ! -d "$SEMANTIC_DIR/dist" ] || [ ! "$(ls -A $SEMANTIC_DIR/dist)" ]; then
      gulp build
    fi
    gulp watch &
    cd /code
    npm run dev
  else
    nginx
  fi
fi

exec "$@"
