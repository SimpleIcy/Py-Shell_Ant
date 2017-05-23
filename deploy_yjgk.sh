#!/bin/bash

#author Gore
#version 1.0
export PATH=$PATH:/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/java/jdk1.7.0_75/bin:/root/bin

echo -e 'PATH:'$PATH
pid_pc=`lsof -i:8088 |tail -n 1 |awk -F' ' '{print $2}'`
pid_dp=`lsof -i:7003 |tail -n 1 |awk -F' ' '{print $2}'`
pid_server=`lsof -i:7002 |tail -n 1 |awk -F' ' '{print $2}'`
wlspath='/home/weblogic/bea/wlserver_10.3/server/lib'

echo $pid_pc,$pid_dp >> /tmp/old_app_pid

if [ -e /tmp/status_all ];then
  rm /tmp/status_all
fi

all(){
  cd /home/weblogic/bea/user_projects/domains/sguap_server/
  nohup ./startWebLogic.sh &
  echo -e
  sleep 25
  echo -e 'server' >> /tmp/status_all
  if [ "$pid_dp" == "" ];then
    cd /home/weblogic/bea/user_projects/domains/yjgk_domain/
    rm nohup.out
    nohup ./startWebLogic.sh &
    echo -e
    sleep 165
    echo -e 'dp' >> /tmp/status_all
  else
    java -cp $wlspath/weblogic.jar weblogic.Deployer -adminurl http://10.176.50.18:7003 -username weblogic -password weblogic2 -name yjgk_domain -redeploy
    echo -e 'dp' >> /tmp/status_all
  fi

  if [ "$pid_pc" == "" ];then
    cd /home/weblogic/bea/user_projects/domains/mcsas/
    rm nohup.out
    nohup ./startWebLogic.sh &
    echo -e
    sleep 265
    echo -e 'pc' >> /tmp/status_all
  else
    java -cp $wlspath/weblogic.jar weblogic.Deployer -adminurl http://10.176.50.18:8088 -username weblogic -password weblogic3 -name mcsas -undeploy
    java -cp $wlspath/weblogic.jar weblogic.Deployer -adminurl http://10.176.50.18:8088 -username weblogic -password weblogic3 -name mcsas -deploy /home/weblogic/yjgk_publish/mcsas
    echo -e 'pc' >> /tmp/status_all
  fi
}

pc(){
  cd /home/weblogic/bea/user_projects/domains/sguap_server/
  rm nohup.out
  nohup ./startWebLogic.sh &
  echo -e
  sleep 25
  echo -e 'server' >> /tmp/status_all
  if [ "$pid_pc" == "" ];then
    cd /home/weblogic/bea/user_projects/domains/mcsas/
    rm nohup.out
    nohup ./startWebLogic.sh &
    echo -e
    sleep 265
    echo -e 'pc' >> /tmp/status_all
  else
    java -cp $wlspath/weblogic.jar weblogic.Deployer -adminurl http://10.176.50.18:8088 -username weblogic -password weblogic3 -name mcsas -undeploy
    java -cp $wlspath/weblogic.jar weblogic.Deployer -adminurl http://10.176.50.18:8088 -username weblogic -password weblogic3 -name mcsas -deploy /home/weblogic/yjgk_publish/mcsas
    echo -e 'pc' >> /tmp/status_all
  fi
}

dp(){
  cd /home/weblogic/bea/user_projects/domains/sguap_server/
  rm nohup.out
  nohup ./startWebLogic.sh &
  echo -e
  sleep 25
  echo -e 'server' >> /tmp/status_all
  if [ "$pid_dp" == "" ];then
    cd /home/weblogic/bea/user_projects/domains/yjgk_domain/
    rm nohup.out
    nohup ./startWebLogic.sh &
    echo -e
    sleep 165
    echo -e 'dp' >> /tmp/status_all
  else
    java -cp $wlspath/weblogic.jar weblogic.Deployer -adminurl http://10.176.50.18:7003 -username weblogic -password weblogic2 -name yjgk_domain -redeploy
    echo -e 'dp' >> /tmp/status_all
  fi
}

stop(){
  echo -e 'PID_Server:',$pid_server > /tmp/old_app_pid
  kill -9 $pid_server
}

 
case "$1" in
  stop)
    stop
    ;;
  pc)
    pc
    ;;
  dp)
    dp
    ;;
  all)
    all
    ;;
  *)
    echo $"Usage: $0 {stop|all|pc|dp}"
    exit 2
esac
