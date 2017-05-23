@echo off
d:
@echo 编译打包发布自助脚本 for 10.176.50.18
@echo 使用者请先编辑D:\select_module_compiler_18.py文件的第10、11、15行，选择是否编包，应用服务器发布的系统及编译和发布哪些模块。
@echo ++++++++++++++++++++++
@echo ++++++++++++++++++++++

set /p input=确认已经编辑完D:\select_module_compiler_18.py请按Y，否请按N:"
if "%input%"=="Y" goto run01
if "%input%"=="N" goto end01

:run01
python select_module_compiler_18.py
pause
exit

:end01
echo "没有编辑D:\select_module_compiler_18.py指定具体打包任务，将退出"
pause
exit