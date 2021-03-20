#!/bin/bash

if [ "$1" == 'build' ]; then
    docker build -f $PWD/docker/postgres.dockerfile -t postgres-local $PWD/docker/
elif [ "$1" == 'refresh' ]; then
    ./devops.sh po
    ./devops.sh ra
    ./devops.sh re
elif [ "$1" == 'po' ]; then
    # host='localhost' dbname='testdb' user='admin' password='admin'
    docker stop postgres || true && docker rm postgres || true;
    docker run --name postgres -p 5432:5432 -d postgres-local;
elif [ "$1" == 're' ]; then
    docker stop some-redis || true && docker rm some-redis || true;
    docker run --name some-redis -p 6379:6379 -d redis
elif [ "$1" == 'ra' ]; then
    docker stop some-rabbit || true && docker rm some-rabbit || true;
    docker run --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 -d rabbitmq:management;
else
    echo 'usage: build | po | ra | re'
fi