#coding:utf-8
#author:Gore
#version:2.5
#DOC：检查并更新大屏和PC版的代码，然后重新生成有新代码更新的模块，重新存放编译日志，建立远程SSH连接，停止主机的weblogic应用，删除旧的jar包，上传新的jar包，并重新发布，启动应用
import os
import time
import paramiko

SVN_PC='svn://10.176.23.68:8443/yjgk/source/trunk/PC2016_V_1.0/'
SVN_DP='svn://10.176.23.68:8443/yjgk/source/trunk/DP2016_V_1.0/'
SVN_MESSAGE='svn://10.176.23.68:8443/yjgk/source/trunk/yjgk_zj'
LOCAL_CODE='D:\package\yjgk\workspace'
NEW_JARS='D:\package\plugin\01_Trunk\yjgk-release-1.0.0\sgyjgk-warehouse\WEB-INF\repository\application\yjgk'
PC_MODULES=['mcsas_bd','mcsas_d2gis','mcsas_newd2gis','mcsas_d3gis','mcsas_framework','mcsas_jh','mcsas_js','mcsas_pd','mcsas_ptzl','mcsas_sczh','mcsas_sd','pms_framework','uap.mxframework.extend']
DP_MODULES=['com.sgcc.yjgk.bddp','com.sgcc.yjgk.jhdp','com.sgcc.yjgk.main','com.sgcc.yjgk.pwdp','com.sgcc.yjgk.sczh','com.sgcc.yjgk.sddp','jsdp','com.sgcc.yjgk.zj']
#DP com.sgcc.pms.framework.base,com.sgcc.pms.framework.isc,com.sgcc.pms.yjgk.jk,com.sgcc.yjgk.excelImport,com.sgcc.yjgk.gg,com.sgcc.yjgk.zj,
CREATED_JARS=[]
CREATED_PC_JARS=[]
CREATED_DP_JARS=[]


os.system('DEL D:\package\yjgk\workspace\compile_log\dp_log.txt') #删除上次大屏的编译日志
os.system('DEL D:\package\yjgk\workspace\compile_log\pc_log.txt') #删除上次PC的编译日志

def get_module_revision(module):
	os.system('C:\get_svninfo.bat %s' % module)
	data=open('E:\ci_tmp\%s.xml' % module)
	a=1
	for i in data:
		if a==17:
			module_revision=i[13:18]
			#return module_revision
			print module_revision
			print '####################'
			return module_revision
			break
		else:
			a=a+1
	data.close()
	

def svn_module_revision(module):
	print 'module value: %s' % module
	os.system('C:\get_svnserverinfo.bat %s %s' % (SVN_PC,module))
	data=open('E:\ci_tmp\svn%s.xml' % module)
	a=1
	for i in data:
		if a==13:
			module_revision=i[13:18]
			#return module_revision
			print module_revision
			return module_revision
			break
		else:
			a=a+1
	data.close()	

def svn_dp_module_revision(module):
	print 'module value: %s' % module
	os.system('C:\get_svnserverinfo.bat %s %s' % (SVN_DP,module))
	data=open('E:\ci_tmp\svn%s.xml' % module)
	a=1
	for i in data:
		if a==13:
			module_revision=i[13:18]
			#return module_revision
			print module_revision
			return module_revision
			break
		else:
			a=a+1
	data.close()


	
def svn_message_module_revision(module):
	print 'module value: %s' % module
	os.system('C:\get_svnserverinfo.bat %s %s' % (SVN_MESSAGE,module))
	data=open('E:\ci_tmp\svn%s.xml' % module)
	a=1
	for i in data:
		if a==13:
			module_revision=i[13:18]
			#return module_revision
			print module_revision
			print '####################'
			return module_revision
			break
		else:
			a=a+1
	data.close()

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
	
	
#定义 sftp 连接函数
def sftp_open( _ssh_fd ):
    return _ssh_fd.open_sftp()

#定义 上传/下载 函数
def sftp_put( _sftp_fd, _put_from_path, _put_to_path ):
    return _sftp_fd.put( _put_from_path, _put_to_path )
def sftp_get( _sftp_fd, _get_from_path, _get_to_path ):
    return _sftp_fd.get( _get_from_path, _get_to_path )
	
#定义 sftp 关闭函数
def sftp_close( _sftp_fd ):
    _sftp_fd.close()
	
#定义 ssh 关闭函数
def ssh_close( _ssh_fd ):
    _ssh_fd.close()
	
for module_name in PC_MODULES:
	if svn_module_revision(module_name)==get_module_revision(module_name):
		print "The module %s has no code update yet" % module_name
		#os.system('D:\package\cmd1\@module_name.cmd')
	else:
		os.system('svn up %s\%s' % (LOCAL_CODE,module_name)) #update code
		time.sleep(1)
		os.system('D:\package\cmd1\%s.cmd' % module_name)
		CREATED_JARS.append(module_name)
		if module_name=='mcsas_d3gis':
			CREATED_PC_JARS.append(module_name)
			CREATED_DP_JARS.append(module_name)
		else:
			CREATED_PC_JARS.append(module_name)
		
		

for module_name in DP_MODULES:
	if svn_dp_module_revision(module_name)==get_module_revision(module_name):
		print "The module %s has no code update yet" % module_name
		#os.system('D:\package\cmd\@module_name.cmd')
	else:
		os.system('svn up %s\%s' % (LOCAL_CODE,module_name)) #update code
		time.sleep(1)
		os.system('D:\package\cmd\%s.cmd' % module_name) #compile the jar package
		CREATED_JARS.append(module_name)
		if module_name=='com.sgcc.yjgk.zj':
			CREATED_JARS.pop(module_name)
			CREATED_DP_JARS.append(module_name)
		else:
			CREATED_DP_JARS.append(module_name)
		
		

#单独处理message模块	
if svn_message_module_revision('com.sgcc.yjgk.message')==get_module_revision('com.sgcc.yjgk.message'):
	print "The module com.sgcc.yjgk.message has no code update yet"
		#os.system('D:\package\cmd\@module_name.cmd')
else:
	os.system('svn up %s\%s' % (LOCAL_CODE,'com.sgcc.yjgk.message')) #update code
	time.sleep(1)
	os.system('D:\package\cmd\com.sgcc.yjgk.message.cmd') #compile the jar package
	CREATED_JARS.append('com.sgcc.yjgk.message')

# CREATED_JARS=['mcsas_framework', 'com.sgcc.yjgk.bddp','com.sgcc.yjgk.jhdp','com.sgcc.yjgk.sddp','com.sgcc.yjgk.message','com.sgcc.yjgk.sczh','mcsas_jh','mcsas_sczh', 'mcsas_sd'] 	
print 'CREATED_JARS: %s ' %  CREATED_JARS
print 'Total Jars: %s '	%	CREATED_JARS.__len__()


#使用命令先停止并删除要更新的weblogic应用服务。然后传送新的Jar包至服务器目录，使用WLST脚本发布应用服务，启动应用服务。
def redeploy_weblogic_app(_ip,_port,_pass,_service):
	sshd = ssh_connect( '%s' % _ip, 'weblogic', 'yjgkweb2016#*' )
	print 'Connect the host:%s successful!' % _ip
	if _service=='dp':
		service_server='sguap_server'
		PATH_MCSAS_SERVER='/home/weblogic/yjgk_publish/%s/WEB-INF/repository/application/yjgk' % service_server
	elif _service=='pc':
		service_server='mcsas-server'
		PATH_MCSAS_SERVER='/home/weblogic/yjgk_publish/%s/WEB-INF/repository/application/mcsas' % service_server
	else:
		print "Your _service is wrong!"
	sshd.exec_command( 'java weblogic.Deployer -adminurl http://%s:%s -username weblogic -password %s  -name %s -undeploy' %(_ip,_port,_pass,service_server) )
	print 'Had undeploy the %s' % service_server
	time.sleep(3)
	sftpd=sftp_open(sshd)
	LOCAL_JARS='D:\\package\\plugin\\01_Trunk\\yjgk-release-1.0.0\\sgyjgk-warehouse\\WEB-INF\\repository\\application\\yjgk'
	if _service == 'dp':
		LOCAL_JARS=CREATED_DP_JARS
	A=os.listdir(LOCAL_JARS)
	for jar in CREATED_JARS:  #rm the old jars and upload new jars
		sshd.exec_command('rm %s/%s*.jar' % ( PATH_MCSAS_SERVER,jar ))  #rm the old jar
		print 'Already remove the old module jar: %s' % jar
		for i in A:
			B=os.path.join(LOCAL_JARS,i)
			if os.path.isfile(B) and jar in B:							#在yjgk生成的jar包目录下，找到具体的包名,并将此包上传到服务器对应目录下
				print 'puting the file %s to server directory %s' % (B,PATH_MCSAS_SERVER)
				sftp_put(sftpd, '%s' % B, '%s/%s' % (PATH_MCSAS_SERVER,i) )
			
	#sshd.exec_command( 'chown -R weblogic:bea /home/weblogic/yjgk_publish/mcsasall-server ')
	sftp_put(sftpd, 'D:\\First_PY\\%s_%s.py' % (_ip[10:],_service), '/opt/%s_%s.py' % (_ip[10:],_service) )
	sshd.exec_command( 'java weblogic.WLST /opt/%s_%s.py' % (_ip[10:],_service))
	sftp_close( sftpd )
	ssh_close( sshd )

redeploy_weblogic_app('10.176.50.13','9002',weblogic7,pc)     #此处为打包13服务器的PC。不需要时，直接将此行注释即可
redeploy_weblogic_app('10.176.50.13','7002',weblogic1,dp)     #此处为打包13服务器的DP。不需要时，直接将此行注释即可
redeploy_weblogic_app('10.176.50.8','8089',weblogic3,pc)      #此处为打包8服务器的PC。不需要时，直接将此行注释即可
redeploy_weblogic_app('10.176.50.8','7002',weblogic1,pc)      #此处为打包13服务器的DP。不需要时，直接将此行注释即可
