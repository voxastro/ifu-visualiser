# Backend setup

## Django installation

First, build a docker image with required Python packages.

```shell
$ docker-compose build
```

Check that everything is working as expected so far.

```shell
$ docker-compose run --rm ifu_api python -m django --version
Creating backend_ifu_api_run ... done
3.2.6
```

`--rm` says that container will be removed upon exit.

The next description below applies only to the creation of a new project.

```shell
$ docker-compose run --rm ifu_api bash
Creating backend_ifu_api_run ... done
root@1b442659d63f:/code# django-admin startproject website .
root@1b442659d63f:/code# python manage.py startapp ifuapp
root@1b442659d63f:/code# ls
Dockerfile  README.md  docker-compose.yml  ifuapp  local.env  manage.py  requirements.txt  website
```
