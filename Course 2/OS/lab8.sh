#!/bin/bash

# Проверка, что переданы начальный и конечный PID
if [ $# -ne 2 ]; then
    echo "Usage: $0 <start_pid> <end_pid>"
    exit 1
fi

# Присваивание переменных
start_pid=$1
end_pid=$2

# Проверка, что переданы корректные числа
if ! [[ $start_pid =~ ^[0-9]+$ ]] || ! [[ $end_pid =~ ^[0-9]+$ ]]; then
    echo "Ошибка: оба аргумента должны быть числами."
    exit 1
fi

# Проверка, что начальный PID меньше или равен конечному
if [ "$start_pid" -gt "$end_pid" ]; then
    echo "Ошибка: начальный PID должен быть меньше или равен конечному."
    exit 1
fi

# Проход по каждому PID в указанном диапазоне
for ((pid=start_pid; pid<=end_pid; pid++)); do
    # Проверяем, существует ли директория для этого PID в /proc
    if [ -d "/proc/$pid" ]; then
        # Получение информации о процессе
        process_name=$(cat /proc/$pid/comm 2>/dev/null)
        process_state=$(awk '{print $3}' /proc/$pid/stat 2>/dev/null)
        thread_count=$(awk '{print $20}' /proc/$pid/stat 2>/dev/null)
        parent_pid=$(awk '{print $4}' /proc/$pid/stat 2>/dev/null)
        
        # Запись информации в файл с именем "process_<pid>.txt"
        output_file="process_$pid.txt"
        {
            echo "Process Name: $process_name"
            echo "Process State: $process_state"
            echo "Thread Count: $thread_count"
            echo "Process ID (PID): $pid"
            echo "Parent Process ID (PPID): $parent_pid"
        } > "$output_file"
        
        echo "Информация о процессе PID=$pid записана в $output_file"
    else
        echo "Процесс PID=$pid не существует."
    fi
done
