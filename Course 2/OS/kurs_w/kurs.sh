#!/bin/bash

# Проверка наличия аргумента
if [ -z "$1" ]; then
  echo "Пример использования: $0 <IP-адрес>"
  exit 1
fi

# Проверка корректности IP-адреса
if [[ ! "$1" =~ ^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$ ]]; then
  echo "Некорректный IP-адрес."
  exit 1
fi

# Запрос к серверу с помощью cURL
response=$(curl -s "https://ipinfo.io/$1")

# Обработка JSON с помощью jq
city=$(echo "$response" | jq -r '.city')
country=$(echo "$response" | jq -r '.country')
loc=$(echo "$response" | jq -r '.loc')
postal=$(echo "$response" | jq -r '.postal')
org=$(echo "$response" | jq -r '.org' | sed 's/AS[0-9]* //')
timezone=$(echo "$response" | jq -r '.timezone')
asn=$(echo "$response" | grep -o '"org": "[^"]*' | sed 's/"org": "AS\([0-9]*\).*/\1/')

# Вывод информации
echo "город: $city,"
echo "страна: $country,"

#Обработка координат
if [[ ! -z "$loc" ]]; then
    lat=$(echo $loc | cut -d ',' -f 1)
    lon=$(echo $loc | cut -d ',' -f 2)
    lat_deg=$(echo "$lat" | cut -d '.' -f 1)
    lat_min=$(echo "scale=0; ($lat - $lat_deg) * 60" | bc)
    lon_deg=$(echo "$lon" | cut -d '.' -f 1)
    lon_min=$(echo "scale=0; ($lon - $lon_deg) * 60" | bc)

    echo "координаты: $lat_deg°$lat_minʹ с.ш. $lon_deg°$lon_minʹ з.д,"
else
    echo "координаты: Недоступно,"
fi

echo "почтовый индекс: $postal,"
echo "организация: $org,"
echo "часовой пояс: $timezone,"
echo "номер автономной зоны: AS$asn"

exit 0