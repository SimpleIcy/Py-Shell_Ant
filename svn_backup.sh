#!/bin/bash
#此脚本以30天的周期备份SVN数据，并自动删除以前的文件
#SVN备份脚本，使用前请先参考自己需求，修改SVN程序及数据所在路径，备份存放路径，SVN项目工程名，及备份的FTP服务器信息

SVNDIR=/data/svn
SVNADMIN=/usr/bin/svnadmin
DATE=`date +%Y-%m-%d`
OLDDATE=`date +%Y-%m-%d -d '-30 days'`
BACKDIR=/data/backup/svn-backup
[ -d ${BACKDIR} ] || mkdir -p ${BACKDIR}
LogFile=${BACKDIR}/svnbak.log
[ -f ${LogFile} ] || touch ${LogFile}
mkdir ${BACKDIR}/${DATE}

for PROJECT in myproject official analysis mypharma
do
  cd $SVNDIR
  $SVNADMIN hotcopy $PROJECT $BACKDIR/$DATE/$PROJECT --clean-logs
  cd $BACKDIR/$DATE
  tar zcvf ${PROJECT}_svn_${DATE}.tar.gz $PROJECT > /dev/null
  rm -rf ${PROJECT}
sleep 2
done

HOST=192.168.3.9
FTP_USERNAME=svn
FTP_PASSWORD=svnback3604

cd${BACKDIR}/${DATE}
ftp -i -n -v << !
open ${HOST}
user ${FTP_USERNAME} ${FTP_PASSWORD}
bin
cd ${OLDDATE}
mdelete *
cd ..
rmdir ${OLDDATE}
mkdir ${DATE}
cd ${DATE}
mput *
bye
!


