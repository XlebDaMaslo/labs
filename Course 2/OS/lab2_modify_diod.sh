#!/bin/bash

#создать копию каталога ISTORS в директории /tmp
cp -r ISTOR /tmp/ISTORS

#лишить всех пользователей всех прав на этот каталог
chmod -R 000 /tmp/ISTORS

#временно даем права владельцу для проверки
#chmod u+rwx /tmp/ISTORS

#проверка результата
echo "Права доступа к каталогу /tmp/ISTORS:"
ls -ld /tmp/ISTORS
ls -lR /tmp/ISTORS

#снова отбираем права владельца, чтобы вернуть каталог в состояние '000'
chmod -R 000 /tmp/ISTORS
