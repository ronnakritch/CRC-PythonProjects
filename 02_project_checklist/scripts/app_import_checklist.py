import pandas as pd
from datetime import datetime, timedelta
from configs.checklist_parameter import SSP, OFM, PWB, B2S, CFR
from sqlalchemy import create_engine, text
import sys
import os
# Dynamically add the project root to the module search path
script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
public_config_dir = os.path.abspath(os.path.join(script_dir, "..", "..",)) # Two level up 
sys.path.append(public_config_dir)
from public_configs.paramter_sql import cloud_db1
# Define the target SQL table name
target_table = 'checklist'
db_url = cloud_db1['conn']
engine = create_engine(db_url)

# Step 1: Read the Excel file and select the SSP sheet, columns A:AN
file_path = r'D:\Users\chironnakrit\Central Group\PST Performance Team - Documents\Apps\checklist_table.xlsx'

# List of parameter sets
parameter_sets = [PWB,SSP, OFM, B2S, CFR]

for params in parameter_sets:

    df = pd.read_excel(file_path, sheet_name=(params['sheetname']), usecols=(params['rcol']))
    df2 = pd.read_excel(file_path, sheet_name='Checklist_mapping', usecols='A:J')
    df= df[df['stcode'].notna()]

    # Step 2: Sort the DataFrame by 'id' column in descending order
    df_sorted = df.sort_values(by='id', ascending=False)
    
    # Convert 'cntdate' and 'checkdate' to datetime objects without formatting
    df_sorted['cntdate'] = pd.to_datetime(df_sorted['cntdate'], errors='coerce', utc=True)
    df_sorted['checkdate'] = pd.to_datetime(df_sorted['checkdate'], errors='coerce', utc=True)

    # Step 4: Remove duplicates based on 'stcode' and 'cntdate'
    df_deduped = df_sorted.loc[df_sorted.groupby(['stcode', 'cntdate'])['id'].idxmax()]

    # Step 5: Format dates after sorting and deduplication
    df_deduped['cntdate'] = df_deduped['cntdate'].dt.strftime('%Y%m%d')
    df_deduped['checkdate'] = df_deduped['checkdate'].dt.strftime('%Y%m%d')

    # Step 4: Unpivot columns E to AN
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

    # Filter 'cntdate' < 5 days
    today = datetime.today()
    five_days_ago = today - timedelta(days=1)
    formatted_date = five_days_ago.strftime('%Y%m%d')
    merged_df = merged_df[merged_df['checkdate'] < formatted_date]

    merged_df['cntdate'] = merged_df['cntdate'].astype(str)
    print(merged_df)
    
     # Execute select from SQL
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT bu, stcode, cntdate FROM planall2 WHERE atype IN ('3F','3Q') AND bu = '{params['sheetname']}'"))
        dfp = pd.DataFrame(result.fetchall(), columns=result.keys())
    #print (dfp)

    dfp['cntdate'] = dfp['cntdate'].astype(str)
    dfp['stcode'] = dfp['stcode'].astype(str)
    
    merged_df = pd.merge(dfp, merged_df, how='left', on=['bu', 'stcode', 'cntdate'], indicator=True)
    merged_df = merged_df[merged_df['checkdate'].notna()]
    keepcolumn = ['id','bu', 'stcode', 'cntdate', 'section', 'no', 'subject', 'subdescription',
                  'weight', 'full', 'act', 'point', 'zone', 'checkdate']
    
    merged_df = merged_df[keepcolumn]
    
    # Execute select from SQL
    with engine.connect() as connection:
        result = connection.execute(text(f'SELECT stcode, cntdate FROM {target_table}'))
        dtf = pd.DataFrame(result.fetchall(), columns=result.keys())

    # Convert 'cntdate' in dtf to string to match 'cntdate' in merged_df
    dtf['cntdate'] = dtf['cntdate'].astype(str)
    dtf['stcode'] = dtf['stcode'].astype(str)

    # Perform a left join between the merged DataFrame and the SQL DataFrame
    final_merged = pd.merge(merged_df, dtf, how='left', on=['stcode', 'cntdate'], indicator=True)

    filtered_df = final_merged[final_merged['_merge'] == 'left_only']
    filtered_df['zone'] = filtered_df['zone'].replace({'F': 'Sale', 'B': 'Back'})

    filtered_df.to_csv(params['csv'])

    filtered_df = filtered_df.drop(columns=['_merge','id'])
    
    # Save the filtered result to CSV (optional or append to SQL)
    filtered_df.to_sql(target_table, engine, if_exists='append', index=False)
    