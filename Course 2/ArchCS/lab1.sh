#!/bin/bash

grep 'PRETTY_NAME' /etc/os-release
grep 'VERSION_ID' /etc/os-release
echo 'kernel architectire:' $(uname -m)

echo -e '\nProcessor information'
grep 'model name' /proc/cpuinfo | uniq
grep 'cpu MHz' /proc/cpuinfo | uniq
echo -n 'number of cores: '; grep 'processor' /proc/cpuinfo | wc -l
grep "cache size" /proc/cpuinfo | uniq

echo -e '\nInformation about the size of RAM'
grep 'MemTotal' /proc/meminfo
grep 'MemAvailable' /proc/meminfo
mt=$(grep MemTotal /proc/meminfo | awk '{print $2}')
ma=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
mu=$((mt - ma))
echo -e "MemUsed: \t$mu KB"

echo -e '\nNetwork connection parameters and speed'
for iface in $(ip -o link show | awk -F': ' '{print $2}'); do
	mac=$(ip link show $iface | awk '/link/ {print $2}')
	ips=$(ip addr show $iface | awk '/inet / {print $2}' | cut -d'/' -f1 | paste -sd, -)
	if command -v ethtool &> /dev/null; then
		speed=$(ethtool $iface | awk '/Speed:/ {print $2}')
	else
		speed='Null'
	fi

	echo "Interface: $iface"
	echo "MAC-address: $mac"
	echo "IP-address: $ips"
    	echo -e "Speed: $speed\n"
done

echo -e '\nInformation about system partitions'
echo -e 'Mounted on \t\t\t Size \t Used \t Avail \t Use%'
df -h | awk 'NR==1 {next} {print $6 " | " $2 " | " $3 " | " $4 " | " $5}' | column -t

echo -e '\nProcessor information:'
grep 'model name' /proc/cpuinfo | uniq
grep 'cpu MHz' /proc/cpuinfo | uniq
echo -n 'Number of logical processors: '
grep 'processor' /proc/cpuinfo | wc -l
grep 'cache size' /proc/cpuinfo | uniq
