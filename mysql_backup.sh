#!/bin/bash

#mysql backup script
#本地周期是20天，ftp周期是60天。

USERNAME=mysqlbackup
PASSWORD=mysqlbackup
DATE=`date +%Y-%m-%d`
OLDDATE=`date +%Y-%m-%d -d '-20 days'`
FTPOLDDATE=`date +%Y-%m-%d -d '-60 days'`
MYSQL=/usr/local/mysql/bin/mysql
MYSQLDUMP=/usr/local/mysql/bin/mysqldump
MYSQLADMIN=/usr/local/mysql/bin/mysqladmin
SOCKET=/tmp/mysql.sock
BACKDIR=/data/backup/db

[ -d ${BACKDIR} ] || mkdir -p ${BACKDIR}
[ -d ${BACKDIR}/${DATE} ] || mkdir ${BACKDIR}/${DATE}
[ ! -d ${BACKDIR}/${OLDDATE} || rm -rf ${BACKDIR}/${OLDDATE}

for DBNAME in mysql test report
do
  ${MYSQLDUMP} --opt -u${USERNAME} -p${PASSWORD} -S${SOCKET} ${DBNAME} | gzip > ${BACKDIR}/${DATE}/${DBNAME}-backup-${DATE}.sql.gz
  echo "${DBNAME} has been backup successful"
  /bin/sleep 5
done

HOST=192.168.3.9
FTP_USERNAME=mysqlback
FTP_PASSWORD=mysqlback
cd ${BACKDIR}/${DATE}
ftp -i -n -v << !
open ${HOST}
user ${FTP_USERNAME} ${FTP_PASSWORD}
bin
cd ${FTPOLDDATE}
mdelete *
cd ..
rmdir ${FTPOLDDATE}
mkdir ${DATE}
mput *
bye
!
