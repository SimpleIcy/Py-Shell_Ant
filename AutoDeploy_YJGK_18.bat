@echo off
d:
@echo ���������������ű� for 10.176.50.18
@echo ʹ�������ȱ༭D:\select_module_compiler_18.py�ļ��ĵ�10��11��15�У�ѡ���Ƿ�����Ӧ�÷�����������ϵͳ������ͷ�����Щģ�顣
@echo ++++++++++++++++++++++
@echo ++++++++++++++++++++++

set /p input=ȷ���Ѿ��༭��D:\select_module_compiler_18.py�밴Y�����밴N:"
if "%input%"=="Y" goto run01
if "%input%"=="N" goto end01

:run01
python select_module_compiler_18.py
pause
exit

:end01
echo "û�б༭D:\select_module_compiler_18.pyָ�����������񣬽��˳�"
pause
exit