#!/bin/bash

if [ -z "$1" ]; then
  echo "Использование: ./stop_and_remove_traefik.sh N"
  exit 1
fi

NUM_CONTAINERS=$1

for i in $(seq 1 $NUM_CONTAINERS); do
  docker stop web$i
  docker rm web$i

  rm index$i.html Dockerfile$i
done

docker stop traefik
docker rm traefik

echo "Все контейнеры и Traefik были остановлены и удалены."
