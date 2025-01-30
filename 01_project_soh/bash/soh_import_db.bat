@echo off
set LOG_FILE=C:\11_Python\01_project_soh\log\soh_import_db.text

cd/d c:\11_Python\01_project_soh\scripts

echo ---------------------------------------------------------------------------------------->>%LOG_FILE%
echo /// batch started : %date% %time%>>%LOG_FILE% ///

echo python app_import_soh_jda.py
echo app_import_soh_jda completed : %date% %time%>> %LOG_FILE%

python app_import_soh_chg_pwb.py
echo app_import_soh_chg_pwb completed : %date% %time%>> %LOG_FILE%

python app_import_soh_sspwds.py
echo app_import_soh_sspwds completed : %date% %time%>> %LOG_FILE%

python app_import_soh_pwb_ussm.py
echo app_import_soh_pwb_ussm completed : %date% %time%>> %LOG_FILE%

python app_export_soh_update.py
echo app_export_soh_update completed : %date% %time%>> %LOG_FILE%

python app_export_soh_update_pwb.py
echo app_export_soh_update_pwb completed : %date% %time%>> %LOG_FILE%

python app_could_import_soh.py
echo app_could_import_soh completed : %date% %time%>> %LOG_FILE%

python app_could_import_soh_pwb_3q.py
echo app_could_import_soh_pwb_3q completed : %date% %time%>> %LOG_FILE%

echo /// batch completed : %date% %time%>> %LOG_FILE% ///

pause