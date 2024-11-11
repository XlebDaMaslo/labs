#!/bin/bash

# Проверка аргумента
if [ -z "$1" ]; then
  echo "Пример команды: ./run_n_containers.sh N"
  exit 1
fi

# Количество контейнеров
NUM_CONTAINERS=$1

# Сеть для контейнеров
docker network ls | grep -w my-network > /dev/null || docker network create my-network

# Генерация контейнеров
for i in $(seq 1 $NUM_CONTAINERS); do
  # Генерация HTML файла
  sed "s/{{NUMBER}}/$i/g" template.html > index$i.html
  
  # Генерация Dockerfile для каждого контейнера
  cat > Dockerfile$i <<EOL
FROM nginx:alpine
COPY index$i.html /usr/share/nginx/html/index.html
EOL

  docker build -t web$i -f Dockerfile$i .

  docker run -d --name web$i --network my-network -p 808$i:80 web$i
done

# Конфигурация Nginx для балансировки запросов
cat > nginx.conf <<EOL
events {}

http {
    upstream backend {
EOL

for i in $(seq 1 $NUM_CONTAINERS); do
  echo "        server web$i:80;" >> nginx.conf
done

cat >> nginx.conf <<EOL
    }

    server {
        listen 80;

        location / {
            proxy_pass http://backend;
        }
    }
}
EOL

docker run -d --name nginx --network my-network -p 80:80 -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro nginx:alpine

echo "Запущено $NUM_CONTAINERS контейнеров (на порту 80)"
