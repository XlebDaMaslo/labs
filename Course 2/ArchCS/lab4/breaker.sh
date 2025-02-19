#!/bin/bash

if [ -z "$1" ]; then
  echo "Использование: ./stop_and_remove_n_containers.sh N"
  exit 1
fi

NUM_CONTAINERS=$1

for i in $(seq 1 $NUM_CONTAINERS); do
  docker stop web$i
  docker rm web$i

  rm index$i.html Dockerfile$i
done

docker stop nginx
docker rm nginx

docker network rm my-network

echo "Все $NUM_CONTAINERS контейнеров остановлены и удалены."
