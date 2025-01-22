@echo off
set LOG_FILE=C:\11_Python\01_project_soh\log\soh_set_jda.text

cd/d c:\11_Python\01_project_soh\scripts

echo ---------------------------------------------------------------------------------------->>%LOG_FILE%
echo /// batch started : %date% %time%>>%LOG_FILE% ///

python app_set_soh_ofm.py
echo app_set_soh_ofm.py completed : %date% %time%>> %LOG_FILE%

python app_set_soh_ssp.py
echo app_set_soh_ssp.py completed : %date% %time%>> %LOG_FILE%

python app_set_soh_b2s.py
echo app_set_soh_b2s.py completed : %date% %time%>> %LOG_FILE%


echo /// batch completed : %date% %time%>> %LOG_FILE% ///

pause

