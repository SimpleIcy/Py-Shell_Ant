#!/bin/bash

#deny ip that connections more than 1000
#结合crond使用，如10分自动执行一次
#此脚本并不好用，单纯只是可以防护而已
netstat -an | grep :25 | grep -v 127.0.0.1 | awk '{ print $5 }' | sort | awk -F: '{ print $1,$4 }' | uniq -c | awk '$1 >50 { print $1,$2}' > /root/black_ip.txt

for i in `awk '{ print $2 }' /root/black_ip.txt`
do
  COUNT=`grep $i /root/black_ip.txt | awk '{ print \$1 }'`
  MAXCONNECTIONS="1000"
  ZERO="0"
  if [ $COUNT -gt $MAXCONNECTIONS ];then
    grep $i /root/white_ip.txt > /dev/null
    if [ $? -gt $ZERO ];then
      echo "$COUNT $i"
      iptables -I INPUT -p tcp -s $i -j drop
    fi
  fi
done
	
