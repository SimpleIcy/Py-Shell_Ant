D:
cd %code_home%\mcsas_sd
if not exist %code_home%\compile_log md %code_home%\compile_log
ant -buildfile build.xml >> %code_home%\compile_log\pc_log.txt
