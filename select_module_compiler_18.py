#coding:utf-8

#author:Gore
#version:3.0
#DOC：检查并更新大屏和PC版的代码，然后重新生成有新代码更新的模块，重新存放编译日志，建立远程SSH连接，停止主机的weblogic应用，删除旧的jar包，上传新的jar包，并重新发布，启动应用
import os
import time
import paramiko

IS_COMPILE=1	 #二个选项0、1分别对应不进行编译压jar包、编译压jar包
App='pc'        #三个选项all、pc、dp分别对应重新发布二个系统、PC系统、大屏系统


#模块配置段	
UPDATEING_JARS=['com.sgcc.mcsas.sd']	#UPDATEING_JARS内配置想要编译打包的模块名
#UPDATEING_JARS=['com.sgcc.mcsas.yjjs','com.sgcc.mcsas.sczh','com.sgcc.mcsas.service','mcsas_ptzl','com.sgcc.yjgk.zj','com.sgcc.mcsas.sd','mcsas_framework']	#UPDATEING_JARS内配置想要编译打包的模块名


PC_MODULES=['mcsas_bd','mcsas_d3gis','mcsas_framework','mcsas_jh','mcsas_js','mcsas_pd','mcsas_ptzl','mcsas_sczh','mcsas_sd','pms_framework','uap.mxframework.extend','com.sgcc.mcsas.sd','com.sgcc.mcsas.sczh','com.sgcc.mcsas.service','com.sgcc.mcsas.pwzy','com.sgcc.mcsas.yjjs','mcsas_customerfeedback','com.sgcc.mcsas.jhzy','mcsas_common','mcsas_xtgl']
NEW_PC_MODULES=['com.sgcc.mcsas.sd','com.sgcc.mcsas.sczh','com.sgcc.mcsas.service']
#'mcsas_common' 'mcsas_d2gis','mcsas_newd2gis' 此三个模块应该是移除系统了
DP_MODULES=['com.sgcc.yjgk.bddp','com.sgcc.yjgk.jhdp','com.sgcc.yjgk.main','com.sgcc.yjgk.pwdp','com.sgcc.yjgk.sczh','com.sgcc.yjgk.sddp','jsdp','com.sgcc.yjgk.zj']
#DP com.sgcc.pms.framework.base,com.sgcc.pms.framework.isc,这二个很少会更新,com.sgcc.yjgk.zj,此模块大屏和PC都会使用
ALLIN_MODULES=['com.sgcc.yjgk.bddp','com.sgcc.yjgk.jhdp','com.sgcc.yjgk.pwdp','com.sgcc.yjgk.sczh','com.sgcc.yjgk.sddp','jsdp','com.sgcc.yjgk.zj','mcsas_d3gis']

#SVN地址配置段
SVN_PC='svn://10.176.23.68:8443/yjgk/source/trunk/PC2016_V_1.0/'
SVN_DP='svn://10.176.23.68:8443/yjgk/source/trunk/DP2016_V_1.0/'
SVN_MESSAGE='svn://10.176.23.68:8443/yjgk/source/trunk/yjgk_zj'

#windows本地代码存放路径和本地新编译出的包路径
LOCAL_CODE='D:\package\yjgk\workspace'
NEW_JARS='D:\package\plugin\01_Trunk\yjgk-release-1.0.0\sgyjgk-warehouse\WEB-INF\repository\application\yjgk'
#PATH_MCSAS_SERVER='/tmp/mcsas'

#服务器上管控系统Jar包放置路径
PATH_MCSAS_SERVER='/home/weblogic/yjgk_publish/sguap_server/WEB-INF/repository/application/mcsas'
PATH_YJGK_SERVER='/home/weblogic/yjgk_publish/sguap_server/WEB-INF/repository/application/yjgk'
CREATED_JARS=[]


os.system('DEL D:\package\yjgk\workspace\compile_log\dp_log.txt') #删除上次大屏的编译日志
os.system('DEL D:\package\yjgk\workspace\compile_log\pc_log.txt') #删除上次PC的编译日志


def compilejar():	
	for module_name in UPDATEING_JARS:
		os.system('svn up %s\%s' % (LOCAL_CODE,module_name)) #update code
		time.sleep(1)
		if module_name in PC_MODULES or module_name in NEW_PC_MODULES:
			os.system('D:\package\cmd1\%s.cmd' % module_name)
			CREATED_JARS.append(module_name)
		else:
			os.system('D:\package\cmd\%s.cmd' % module_name) #compile the jar package
			CREATED_JARS.append(module_name)

			
		
#定义 ssh 连接函数
def ssh_connect( _host, _username, _password ):
    try:
        _ssh_fd = paramiko.SSHClient()
        _ssh_fd.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
        _ssh_fd.connect( _host, username = _username, password = _password )
    except Exception, e:
        print( 'ssh %s@%s: %s' % (_username, _host, e) )
        exit()
    return _ssh_fd	

#定义 ssh 关闭函数
def ssh_close( _ssh_fd ):
    _ssh_fd.close()


# CREATED_JARS为打包生成的新jar包模块名数组
if IS_COMPILE==1:
	compilejar()	
print 'CREATED_JARS: %s ' %  CREATED_JARS
print 'Total Jars: %s '	%	CREATED_JARS.__len__()
time.sleep(5)
	
ssh01=ssh_connect('10.176.50.18','weblogic','yjgkweb2016#*')
print 'ssh01 Connect the host:10.176.50.18 successful!'  
 
for jar in UPDATEING_JARS:  #backup and rm the old jars
	if jar in PC_MODULES and jar not in ALLIN_MODULES:
		ssh01.exec_command('cp %s/%s*.jar /home/weblogic/old_jars/' % ( PATH_MCSAS_SERVER,jar ))
		ssh01.exec_command('rm %s/%s*.jar' % ( PATH_MCSAS_SERVER,jar ))
		print 'backup and rm %s/%s*.jar' % ( PATH_MCSAS_SERVER,jar )
	elif jar in ALLIN_MODULES:
		ssh01.exec_command('cp %s/%s*.jar /home/weblogic/old_jars/' % ( PATH_MCSAS_SERVER,jar ))
		ssh01.exec_command('rm %s/%s*.jar' % ( PATH_MCSAS_SERVER,jar )) 
		ssh01.exec_command('rm %s/%s*.jar' % ( PATH_YJGK_SERVER,jar ))
		print 'backup and rm %s/%s*.jar' % ( PATH_MCSAS_SERVER,jar )
		print 'backup and rm %s/%s*.jar' % ( PATH_YJGK_SERVER,jar )
	elif jar in DP_MODULES:
		ssh01.exec_command('cp %s/%s*.jar /home/weblogic/old_jars/' % ( PATH_YJGK_SERVER,jar ))
		ssh01.exec_command('rm %s/%s*.jar' % ( PATH_YJGK_SERVER,jar ))
		print 'backup and rm %s/%s*.jar' % ( PATH_YJGK_SERVER,jar )
ssh_close(ssh01)
client = paramiko.Transport(('10.176.50.18',22))
client.connect(username = 'weblogic',password = 'yjgkweb2016#*')
sftp = paramiko.SFTPClient.from_transport(client)
LOCAL_JARS='D:\\package\\plugin\\01_Trunk\\yjgk-release-1.0.0\\sgyjgk-warehouse\\WEB-INF\\repository\\application\\yjgk'
A=os.listdir(LOCAL_JARS)
os.chdir(LOCAL_JARS)
for jar in UPDATEING_JARS:  #upload new jars
	for i in A:
		B=os.path.join(LOCAL_JARS,i)
		if os.path.isfile(B) and jar in B:							#在yjgk生成的jar包目录下，找到具体的包名,并将此包上传到服务器对应目录下
			if jar in PC_MODULES and jar not in ALLIN_MODULES:
				print 'transfering ',i
				sftp.put( '%s' % i, '%s/%s' % (PATH_MCSAS_SERVER,i) )
			elif jar in ALLIN_MODULES:
				print 'transfering ',i
				sftp.put( '%s' % i, '%s/%s' % (PATH_MCSAS_SERVER,i) )
				sftp.put( '%s' % i, '%s/%s' % (PATH_YJGK_SERVER,i) )
			elif jar in DP_MODULES:
				print 'transfering ',i
				sftp.put( '%s' % i, '%s/%s' % (PATH_MCSAS_SERVER,i) )

time.sleep(10)
client.close()
ssh02 = ssh_connect( '10.176.50.18', 'weblogic', 'yjgkweb2016#*' )
print 'ssh02 Connect the host:10.176.50.18 successful!'
ssh02.exec_command('/bin/bash /tmp/deploy_yjgk.sh stop')
print 'Had stop the sguap_server'
time.sleep(20)
if App=='all': 
	print 'Reploying the DP and PC...'
	ssh02.exec_command('/bin/bash /tmp/deploy_yjgk.sh all')  #stop the weblogic server
	time.sleep(470)
	all1,all2,all3=ssh02.exec_command('/bin/cat /tmp/status_all')
	print 'Servers which had redeployed:'
	print all2.read()
elif App=='pc':
	print 'Reploying the PC...'
	ssh02.exec_command('/bin/bash /tmp/deploy_yjgk.sh pc')
	time.sleep(265)
	pc1,pc2,pc3=ssh02.exec_command('/bin/cat /tmp/status_all')
	print 'Servers which had redeployed:'
	print pc2.read()
elif App=='dp':
	print 'Reploying the DP...'
	ssh02.exec_command('/bin/bash /tmp/deploy_yjgk.sh dp')  #stop the weblogic server
	time.sleep(190)
	dp1,dp2,dp3=ssh02.exec_command('/bin/cat /tmp/status_all')
	print 'Servers which had redeployed:'
	print dp2.read()
print 'Finishing the Deployment Work!!!'
time.sleep(5)
ssh_close( ssh02 )


#单独处理message模块	
# if svn_message_module_revision('com.sgcc.yjgk.message')==get_module_revision('com.sgcc.yjgk.message'):
	# print "The module com.sgcc.yjgk.message has no code update yet"
		# #os.system('D:\package\cmd\@module_name.cmd')
# else:
	# os.system('svn up %s\%s' % (LOCAL_CODE,'com.sgcc.yjgk.message')) #update code
	# time.sleep(1)
	# os.system('D:\package\cmd\com.sgcc.yjgk.message.cmd') #compile the jar package
	# CREATED_JARS.append('com.sgcc.yjgk.message')
