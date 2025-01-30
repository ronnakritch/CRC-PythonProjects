import pandas as pd
from sqlalchemy import create_engine, text

import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
# Project root (one level up)
project_root = os.path.abspath(os.path.join(script_dir, ".."))
# Public config directory (two levels up)
public_config_dir = os.path.abspath(os.path.join(script_dir, "..", "..",))
sys.path.append(project_root)
sys.path.append(public_config_dir)

from public_configs.paramter_sql import cloud_db1,local_db1
from configs.parameter_soh_chg_pwb import CHG_parameter, PWB_parameter

# Define the target SQL
db_url = local_db1['conn']
engine = create_engine(db_url)

db_url2 = cloud_db1['conn']
engine2 = create_engine(db_url2)

# List of parameter sets
parameter_sets = [CHG_parameter] #PWB_parameter, 

for params in parameter_sets:

    df = pd.read_csv(params["raw_file"], encoding='cp874')
    df = df.applymap(lambda x: x.lstrip("'") if isinstance(x, str) else x)
    df = df[df[params["soh_col"]] != 0]
    
    # Convert column names to lowercase
    df.columns = df.columns.str.lower()
    
    #change format type
    df['msstor'] = df['msstor'].astype(str)
    df['msasdt'] = df['msasdt'].astype(str)

    with engine2.connect() as connection:
        result = connection.execute(text(f'SELECT stcode, "DATE" FROM soh_update'))
        dfs = pd.DataFrame(result.fetchall(), columns=result.keys())
 
    #change format type
    dfs['msstor'] = dfs['stcode'].astype(str)
    dfs['msasdt'] = dfs['DATE'].astype(str)

    merged_df = df.merge(dfs, how='left', on=['msstor', 'msasdt'], indicator=True) 

    #Filter rows that are only in the Excel file (not in the database)
    filtered_df = merged_df[merged_df['_merge'] == 'left_only']
    # Drop unnecessary columns from the merged DataFrame
    filtered_df = filtered_df.drop(columns=['stcode', 'DATE','_merge'])
    print(filtered_df)
    
    # Output the filtered DataFrame to a CSV file
    output_csv = params["convert_file"]
    filtered_df.to_csv(output_csv, index=False)

    # Insert the data into the SQL table
    target_table = params["sql_table"]
    filtered_df.to_sql(target_table, engine, if_exists='append', index=False)

    print(f"Insert to {target_table} completed")