@echo off
set LOG_FILE=C:\11_Python\01_project_soh\log\soh_import_db.text

cd/d c:\11_Python\01_project_soh\script

echo ---------------------------------------------------------------------------------------->>%LOG_FILE%
echo /// batch started : %date% %time%>>%LOG_FILE% ///

echo python app_import_soh_jda.py
echo app_import_soh_jda completed : %date% %time%>> %LOG_FILE%

python app_import_soh_chg_pwb.py
echo app_import_soh_chg_pwb completed : %date% %time%>> %LOG_FILE%

python app_import_soh_sspwds.py
echo app_import_soh_sspwds completed : %date% %time%>> %LOG_FILE%

python app_export_soh_update.py
echo app_export_soh_update completed : %date% %time%>> %LOG_FILE%

python app_import_soh_could.py
echo app_import_soh_could completed : %date% %time%>> %LOG_FILE%

echo /// batch completed : %date% %time%>> %LOG_FILE% ///

pause