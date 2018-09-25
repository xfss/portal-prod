build:
		@USER_ID=$(shell id -u) docker-compose -f docker-compose.yml -f docker-compose.local.yml build

run:
		@USER_ID=$(shell id -u) docker-compose -f docker-compose.yml -f docker-compose.local.yml -f dev.secrets.yml -p localpoint-portal up

run-d:
		@USER_ID=$(shell id -u) docker-compose -f docker-compose.yml -f docker-compose.local.yml -f dev.secrets.yml -p localpoint-portal up -d

run-dev-d:
		@USER_ID=$(shell id -u) docker-compose -f docker-compose.yml -f docker-compose.master.yml -f dev.secrets.yml -p localpoint-portal-dev up -d

run-prod-d:
		@USER_ID=$(shell id -u) docker-compose -f docker-compose.yml -f docker-compose.prod.yml -f prod.secrets.yml -p localpoint-portal-prod up -d

pull-dev:
		@USER_ID=$(shell id -u) docker-compose -f docker-compose.yml -f docker-compose.master.yml -f dev.secrets.yml -p localpoint-portal-dev pull backend frontend

pull-prod:
		@USER_ID=$(shell id -u) docker-compose -f docker-compose.yml -f docker-compose.prod.yml -f prod.secrets.yml -p localpoint-portal-prod pull backend frontend

logs:
		@docker logs -f --tail=200 localpoint-portal

bash:
		@docker exec -it localpoint-portal bash

stop:
		@USER_ID=$(shell id -u) docker-compose -p localpoint-portal stop

down:
		@USER_ID=$(shell id -u) docker-compose -p localpoint-portal down

default: build
