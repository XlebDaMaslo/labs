#!/bin/bash
{
  PRETTY_NAME=$(grep 'PRETTY_NAME' /etc/os-release | cut -d'=' -f2 | tr -d '"')
  VERSION_ID=$(grep 'VERSION_ID' /etc/os-release | cut -d'=' -f2)
  echo "PRETTY_NAME=$PRETTY_NAME"
  echo "VERSION_ID=$VERSION_ID"
  echo "kernel architecture: $(uname -m)"
  echo -e '\nProcessor information'
  NUM_SOCKETS=$(grep 'physical id' /proc/cpuinfo | sort -nu | wc -l)
  for ((i=0; i < NUM_SOCKETS; i++)); do
    echo "Socket $i"
    grep 'model name' /proc/cpuinfo | uniq
    grep 'cpu MHz' /proc/cpuinfo | uniq
    echo -n 'number of cores: '; grep 'processor' /proc/cpuinfo | wc -l
    grep "cache size" /proc/cpuinfo | uniq
  done
  echo -e '\nInformation about the size of RAM'
  grep 'MemTotal' /proc/meminfo
  grep 'MemAvailable' /proc/meminfo
  mt=$(grep MemTotal /proc/meminfo | awk '{print $2}')
  ma=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
  mu=$((mt - ma))
  echo -e "MemUsed: \t$mu KB"
  echo -e '\nNetwork connection parameters and speed'
  for iface in $(ls -1 /sys/class/net); do
    mac=$(ifconfig $iface | awk '/ether/ {print $2}')
    ips=$(ifconfig $iface | awk '/inet / {print $2}')
    speed='Unknown'
    echo "Interface: $iface"
    echo "MAC-address: $mac"
    echo "IP-address: $ips"
    echo -e "Speed: $speed\n"
  done
  echo -e '\nInformation about system partitions'
  echo -e 'Mounted on \t\t\t Size \t Used \t Avail \t Use%'
  df -h | awk 'NR==1 {next} {print $6 " | " $2 " | " $3 " | " $4 " | " $5}'
} > /tmp/lab1_output.txt
