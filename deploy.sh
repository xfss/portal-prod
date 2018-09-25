#!/bin/bash

SSH_USER=portal
HOST="$1"
ENV="$2"
BRANCH=
PATH=/srv/portal/$ENV

if [[ "$ENV" == "dev" ]]; then
  BRANCH="${BRANCH:-master}"
elif [[ "$ENV" == "prod" ]]; then
  BRANCH="${BRANCH:-prod}"
else
  echo "Settings should be 'dev' or 'prod'"
  exit 1
fi

/usr/bin/ssh -vt "$SSH_USER@$HOST" <<EOF
docker login -u gitlab-ci-token -p $CI_JOB_TOKEN registry.consenda.com
cd "$PATH"
echo "Pulling from git"
git fetch --all
git checkout $BRANCH
git reset --hard
git pull origin $BRANCH
echo "Pulling images from registry"
make pull-$ENV
echo "Start/restart containers"
make run-$ENV-d
EOF
