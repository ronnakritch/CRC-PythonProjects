import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
import csv

import sys
import os
# Dynamically add the project root to the module search path
script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
project_root = os.path.abspath(os.path.join(script_dir, ".."))  # One level up (project root)
sys.path.append(project_root)  # Add project root to sys.path
public_config_dir = os.path.abspath(os.path.join(script_dir, "..", "..",)) # Two level up 
sys.path.append(public_config_dir)
from public_configs.paramter_sql import cloud_db1
from configs.checklist_parameter import SSP, OFM, PWB, B2S, CFR

# SQL and Log Configuration
log_table = "log_checklist"
db_url = cloud_db1['conn']
engine = create_engine(db_url)

def log_to_sql(start_time, end_time, duration, bu, stcode_count, record_count, status, no_count, error_message=""):
    log_entry = pd.DataFrame([{
        "start_time": start_time,
        "end_time": end_time,
        "duration": duration,
        "bu": bu,
        "stcode_count": stcode_count,
        "record_count": record_count,
        "status": status,
        "no_count": no_count,
        "error_message": error_message
    }])
    log_entry.to_sql(log_table, engine, if_exists='append', index=False)

# Target SQL table and Excel file path
target_table = 'checklist'
file_path = r'C:\Users\Administrator\Central Group\PST Performance Team - Documents\Apps\checklist_table.xlsx'

# List of parameter sets
parameter_sets = [PWB, SSP, OFM, B2S, CFR]

for params in parameter_sets:
    start_time = datetime.now()
    bu = params['sheetname']
    try:
        # Step 1: Read the Excel file and filter data
        df = pd.read_excel(file_path, sheet_name=bu, usecols=params['rcol'])
        df2 = pd.read_excel(file_path, sheet_name='Checklist_mapping', usecols='A:J')
        df = df[df['stcode'].notna()]

        # Step 2: Sort by 'id' column in descending order
        df_sorted = df.sort_values(by='id', ascending=False)

        # Convert dates
        df_sorted['cntdate'] = pd.to_datetime(df_sorted['cntdate'], errors='coerce', utc=True)
        df_sorted['checkdate'] = pd.to_datetime(df_sorted['checkdate'], errors='coerce', utc=True)

        # Remove duplicates
        df_deduped = df_sorted.loc[df_sorted.groupby(['stcode', 'cntdate'])['id'].idxmax()]

        # Format dates
        df_deduped['cntdate'] = df_deduped['cntdate'].dt.strftime('%Y%m%d')
        df_deduped['checkdate'] = df_deduped['checkdate'].dt.strftime('%Y%m%d')

        # Unpivot columns
        df_unpivoted = df_deduped.melt(
            id_vars=['id', 'employee_code', 'stcode', 'cntdate', 'checkdate'],
            var_name='checklist_no',
            value_name='point'
        )

        df_sorted2 = df_unpivoted.sort_values(by=['stcode', 'cntdate', 'checklist_no'], ascending=False)

        # Merge with the checklist mapping
        merged_df = pd.merge(df_sorted2, df2, left_on='checklist_no', right_on='Code', how='left')
        merged_df['bu'] = merged_df['BU']
        merged_df['stcode'] = merged_df['stcode'].astype(str).str.zfill(params['st_digit'])
        merged_df['no'] = merged_df['NO']
        merged_df['zone'] = merged_df['ZONE']
        merged_df['full'] = merged_df['Point']
        merged_df['weight'] = merged_df['Weight']
        merged_df['act'] = merged_df['point'] * merged_df['weight']
        merged_df['section'] = merged_df['Subject']
        merged_df['subject'] = merged_df['Desceiption']
        merged_df['subdescription'] = merged_df['SubDescription']

        # Filter for 'checkdate' less than 5 days ago
        today = datetime.today()
        five_days_ago = today - timedelta(days=1)
        formatted_date = five_days_ago.strftime('%Y%m%d')
        merged_df = merged_df[merged_df['checkdate'] < formatted_date]

        # Execute select from SQL for comparison
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT bu, stcode, cntdate FROM planall2 WHERE atype IN ('3F','3Q') AND bu = '{bu}'"))
            dfp = pd.DataFrame(result.fetchall(), columns=result.keys())

        dfp['cntdate'] = dfp['cntdate'].astype(str)
        dfp['stcode'] = dfp['stcode'].astype(str)

        merged_df = pd.merge(dfp, merged_df, how='left', on=['bu', 'stcode', 'cntdate'], indicator=True)
        merged_df = merged_df[merged_df['checkdate'].notna()]
        keepcolumn = ['id', 'bu', 'stcode', 'cntdate', 'section', 'no', 'subject', 'subdescription',
                      'weight', 'full', 'act', 'point', 'zone', 'checkdate']

        merged_df = merged_df[keepcolumn]

        # Execute select from SQL for deduplication
        with engine.connect() as connection:
            result = connection.execute(text(f'SELECT stcode, cntdate FROM {target_table}'))
            dtf = pd.DataFrame(result.fetchall(), columns=result.keys())

        dtf['cntdate'] = dtf['cntdate'].astype(str)
        dtf['stcode'] = dtf['stcode'].astype(str)

        # Perform a left join
        final_merged = pd.merge(merged_df, dtf, how='left', on=['stcode', 'cntdate'], indicator=True)

        filtered_df = final_merged[final_merged['_merge'] == 'left_only']
        filtered_df['zone'] = filtered_df['zone'].replace({'F': 'Sale', 'B': 'Back'})

        # Count the number of 'no' records
        no_count = filtered_df['no'].count()

        filtered_df.to_sql(target_table, engine, if_exists='append', index=False)
        stcode_count = filtered_df['stcode'].nunique()
        # Log success entry
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        log_to_sql(start_time, end_time, duration, bu, stcode_count, len(filtered_df), "complete", no_count)

    except Exception as e:
        # Log failure entry
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        log_to_sql(start_time, end_time, duration, bu, 0, 0, "failed", 0, str(e))