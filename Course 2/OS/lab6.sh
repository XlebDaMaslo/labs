#!/bin/bash

# Информация о пользователе
NAME="Name Surname"
GROUP="123456"

# Функция для вывода справки по использованию скрипта
usage() {
    echo "Пример использования: $0 [-f name] [-d directory]"
    exit 1
}

while getopts ":f:d:" opt; do
  case ${opt} in
    f)
      # Опция -f передана: выводим данные о пользователе
      echo "Имя: $NAME"
      echo "Номер группы: $GROUP"
      ;;
    d)
      # Опция -d передана: проверяем наличие каталога и выводим его содержимое
      if [ -d "$OPTARG" ]; then
        echo "Содержимое каталога $OPTARG:"
        ls "$OPTARG"
      else
        echo "Ошибка: Каталог $OPTARG не существует."
      fi
      ;;
    \?)
      # Неизвестная опция
      echo "Недопустимая опция: -$OPTARG" >&2
      usage
      ;;
    :)
      # Опция без необходимого параметра
      echo "Ошибка: Опция -$OPTARG требует аргумент." >&2
      usage
      ;;
  esac
done

# Если ни одна опция не передана
if [ $OPTIND -eq 1 ]; then
  usage
fi
