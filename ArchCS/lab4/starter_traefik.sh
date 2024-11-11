#!/bin/bash

# Check if the number of containers is provided
if [ -z "$1" ]; then
  echo "Usage: ./run_traefik.sh N"
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
    -l "traefik.http.routers.web$i.rule=Host(\`web$i.local\`)" \
    -l "traefik.http.services.web$i.loadbalancer.server.port=80" \
    web$i
done

echo "Started $NUM_CONTAINERS containers with Traefik. Traefik is running on port 80 and 8080 (for metrics)."
echo "Metrics are available at: http://localhost:8080/metrics"
echo "Access logs are enabled in the Traefik configuration."
echo "You can access the containers at: http://web1.local, http://web2.local, ..."