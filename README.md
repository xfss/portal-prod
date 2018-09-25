# Development

## Docker setup

Docker config is in the docker-compose.yml file, but be aware that data volumes may need changes.
By default Minio volumes are saved under /opt/minio and Postgres volumes are saved under /opt/postgres
These can be changed to anything convenient, the role of these directories to keep config and data for the Minio and Postgres containers so they are not lost when redeploying containers.

After the initial config the containers can be brought up with the following command:

    docker-compose up -d

For minio to work with any frontend and django storages the "minio" domain should be binded to 127.0.0.1

So on linux the /etc/hosts file should contain the following:

    127.0.0.1       minio

There are some ports bound to 0.0.0.0 for convenience, these ports are:

    Backend:    8080
    Frontend:   80
    Postgres:   5432
    Minio:      9000


## Coreapi docs

Coreapi docs contains some errors regarding actions for the js api.
Nesting is broken and the example code is malformed as it contains api routes concatenated with &gt; instead of splitting it up to different strings in the action list.

Example:

For auth login create API the actions are presented like this:
```javascript
var action = ["auth", "login &gt; create"]
```

But in reality it should be used like this:
```javascript
var action = ['auth', 'login', 'create']
```

Notice how we are using single quotes instead of double quotes too, because of our current eslint rules.

## Default admin user and admin interface

Portal django admin can be reached at http://localhost:8080/admin for the dev environment.
To access this admin interface. An admin user should be created.

To create a new admin sure outside of docker, manage.py should be used after running migration

    python3 backend/manage.py migrate
    python3 backend/manage.py createsuperuser

For docker a default admin is automatically created and the migrations are run at every start.
The default superuser credentials are the following:

    username: sa
    password: sa

## Docker

#### NGINX Reverse proxy
If not done already, create a network to be used to connect containers

*  `docker network create nginx_proxy`
   *  This must be the same name set in network section in `docker-compose`
*  `docker run -d -p 80:80 --name=nginx-reverse-proxy --network=nginx_proxy -v /var/run/docker.sock:/tmp/docker.sock:ro jwilder/nginx-proxy`
   *  `--name` parameter is optional but recommended
   *  Adding `--restart=always` will make the container restart after reboot

#### Project
Use `Make` of the equivalent `docker-compose` command:
1.  `make build` (docker-compose build) builds images
2.  `make run` (docker-compose -p localpoint-portal up) runs container
3.  Make sure the domains set as `VIRTUAL_HOST` in the docker-compose file are pointing to `127.0.0.1` in your host's host file
4.  Access the sites with the domains set as `VIRTUAL_HOST`:
   *  http://portal.localpoint.local
   *  http://minio.portal.localpoint.local
   *  http://backend.portal.localpoint.local
5. Setting the `ENVIRONMENT` variable in `frontend` will change the way the service is run:
   *  `dev` will expose the service with `npm run dev` and hot reload
   *  `prod` will serve built files with nginx

6. An additional compose file named `*.secrets.yml` must be created for each environment and **must not** be committed to version control.
   *  `Makefile` has been updated with compose file for dev environment.