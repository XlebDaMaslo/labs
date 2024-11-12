#!/bin/bash

if [ -z "$1" ]; then
  echo "Пример команды: ./run_traefik.sh N"
  exit 1
fi

NUM_CONTAINERS=$1
mkdir -p traefik

cat > traefik/traefik.yml <<EOL
api:
  insecure: true

entryPoints:
  web:
    address: ":80"

metrics:
  prometheus: {}

accessLog: {}

providers:
  docker:
    exposedByDefault: false
EOL

docker run -d \
  --name traefik \
  --network bridge \
  -p 80:80 \
  -p 8080:8080 \
  -v $(pwd)/traefik/traefik.yml:/etc/traefik/traefik.yml \
  -v /var/run/docker.sock:/var/run/docker.sock \
  traefik:v2.10

for i in $(seq 1 $NUM_CONTAINERS); do
  sed "s/{{NUMBER}}/$i/g" template.html > index$i.html

  cat > Dockerfile$i <<EOL
FROM nginx:alpine
COPY index$i.html /usr/share/nginx/html/index.html
EOL

  docker build -t web$i -f Dockerfile$i .

  docker run -d \
    --name web$i \
    --network bridge \
    -l "traefik.enable=true" \
    -l "traefik.http.routers.myweb.rule=Host(\`localhost\`)" \
    -l "traefik.http.services.myweb.loadbalancer.server.port=80" \
    web$i
done

echo "Запущено $NUM_CONTAINERS контейнеров с балансировкой на localhost через Traefik (порт 80)"
