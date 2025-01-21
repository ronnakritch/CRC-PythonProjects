import pandas as pd
import shutil
from psycopg2.extras import execute_values
from sqlalchemy import create_engine, text

import sys
import os
# Dynamically add the project root to the module search path
script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
project_root = os.path.abspath(os.path.join(script_dir, ".."))  # One level up (project root)
sys.path.append(project_root)  # Add project root to sys.path

from configs.parameter_soh_jda import OFM_parameter, B2S_parameter, SSP_parameter

# Define the target SQL table name
db_url = 'postgresql+psycopg2://chironnakrit:20309925@AUDCRCHA0020015/pstdb2' 
engine = create_engine(db_url)

# List of parameter sets
parameter_sets = [OFM_parameter, B2S_parameter, SSP_parameter]

for params in parameter_sets:

    target_table = params['sql_table']
    
    # Check if the file exists
    if not os.path.exists(params["raw_file"]):
        print(f"Error: The file '{params['raw_file']}' does not exist.")
        continue

    try:
        column_names = params["col_name"]

        lowercase_columns = [col.lower() for col in column_names]

        df = pd.read_csv(params["raw_file"], header=None, names=lowercase_columns, encoding='cp874')

        # filter soh <> 0 
        df2 = df[df[params["soh_col"]] != 0 ] 

        
    except Exception as e:
        print(f"Error reading or processing CSV file: {e}")
        continue  
    
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT distinct {params['stcode']}, {params['date']} FROM {target_table}"))
        df_db = pd.DataFrame(result.fetchall(), columns=result.keys())

    df2[[params['stcode'], params['date']]] = df2[[params['stcode'], params['date']]].astype(str)
    df_db[[params['stcode'], params['date']]] = df_db[[params['stcode'], params['date']]].astype(str)

    # Perform left join between df2 and df_db, keeping only rows from df2 that do not match df_db
    df_merged = df2.merge(df_db, how='left', on=[params['stcode'], params['date']], indicator=True) 
    df_left_only = df_merged[df_merged['_merge'] == 'left_only'].drop(columns=['_merge'])
    print(f"Prepare for'{params['sql_table']}'.")


    df_left_only .to_csv(params["convert_file"], index=False)
    print(f"Convert The file CSV '{params['convert_file']}' completed.")

    # Save the result back to the database if needed
    df_left_only.to_sql(target_table, engine, if_exists='append', index=False)
    print(f"insert to'{params['sql_table']}' completed.")
   
    shutil.copy(params["raw_file"], params["old_file"])

