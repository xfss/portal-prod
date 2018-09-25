#!/bin/ash

if [ "$1" = 'start' ]; then
  confd -onetime -backend env -confdir='/code/confd'

  if [[ $ENVIRONMENT == "local" ]]; then
    python3 manage.py makemigrations
  fi

  gosu www-data python3 manage.py migrate
  gosu www-data python3 manage.py collectstatic -v0 --noinput

  # Start cron service and add django crontab tasks
  crond -S
  python3 manage.py crontab add

  # Compile localization files
  python3 manage.py compilemessages


  if [[ $ENVIRONMENT == "local" ]]; then
    python3 manage.py shell < create_default_superuser.py
    python3 manage.py runserver 0.0.0.0:80
  else
    exec forego start -r
  fi
fi

exec "$@"
