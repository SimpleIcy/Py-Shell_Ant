#coding:uft-8
#author:Gore
#Version:1.0
# 8. pc
import time

connect('weblogic','weblogic3','http://10.176.50.8:8089')
undeploy('mcsas-server')
distributeApplication('/home/weblogic/yjgk_publish/mcsas-server/')
startApplication('mcsas-server')
time.sleep(25)
connect('weblogic','weblogic4','http://10.176.50.8:8088')
undeploy('mcsas')
distributeApplication('/home/weblogic/yjgk_publish/mcsas/')
time.sleep(25)
startApplication('mcsas')
exit()