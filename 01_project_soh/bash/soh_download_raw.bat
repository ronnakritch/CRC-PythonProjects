
@echo off
set LOG_FILE=C:\11_Python\01_project_soh\log\soh_load_ibm.text

cd/d c:\11_Python\01_project_soh\scripts

echo ---------------------------------------------------------------------------------------->>%LOG_FILE%
echo /// batch started : %date% %time%>>%LOG_FILE% ///

python app_load_soh_chg_pwb.py
echo python app_load_soh_chg_pwb completed : %date% %time%>> %LOG_FILE%

python app_load_soh_sspwds.py
echo python app_load_soh_sspwds completed : %date% %time%>> %LOG_FILE%

echo python app_load_soh_jda.py
echo python app_load_soh_jda completed : %date% %time%>> %LOG_FILE%


echo /// batch completed : %date% %time%>> %LOG_FILE% ///