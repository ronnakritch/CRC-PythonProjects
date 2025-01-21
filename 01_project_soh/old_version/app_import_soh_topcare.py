import pandas as pd
import os
from datetime import datetime
from sqlalchemy import create_engine, text

# Define the target SQL table name
target_table = 'topscare_soh'
db_url = 'postgresql+psycopg2://chironnakrit:20309925@AUDCRCHA0020015/pstdb2'
engine = create_engine(db_url)

path = r'D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\06_RAW_FILE\SOH\Topcare'
 
# Get a list of all Excel files in the folder
file_list = [f for f in os.listdir(path) if f.endswith('.xlsx') or f.endswith('.xls')]

# Initialize an empty DataFrame to hold all data
combined_df = pd.DataFrame()

for file in file_list:
    file_path = os.path.join(path, file)
    
    # Load the data from each Excel file, skipping the first row
    df = pd.read_excel(file_path, skiprows=[0])  
    
    # Rename the columns to the required names
    df.columns = [
        "sku", "description", "barcode", "unit", "pack", "dept", "sdept", 
        "category", "retail", "brand", "sdept2", "soh", "cost"
    ]
    
    # filename first 5 characters as 'stcode'
    df['stcode'] = file[:6]
    
    # Add a new column for the current date as 'data_date'
    df['data_date'] = datetime.now().strftime("%Y%m%d")
    
    #------------------------------------------------------------------------
    # Execute select from SQL
    with engine.connect() as connection:
        result = connection.execute(text(f'SELECT stcode, data_date as data_date FROM {target_table}'))
        dtf = pd.DataFrame(result.fetchall(), columns=result.keys())

    # Convert 'DATE' in dtf to string to match 'data_date' in df (if necessary)
    dtf['data_date'] = dtf['data_date'].astype(str)

    # Perform a left join between the CSV DataFrame and the SQL DataFrame
    merged_df = df.merge(dtf, how='left',on=['stcode', 'data_date'],indicator= True)
    
    filtered_df = merged_df[merged_df['soh'] != 0 ]
    filtered_df = filtered_df[filtered_df['_merge'] == 'left_only']
    filtered_df = filtered_df.drop(columns = ['_merge']) 
    
    filtered_df.to_csv()
    filtered_df.to_sql(target_table, engine, if_exists='append', index=False)
    print(filtered_df)

import shutil
import os

def copy_all_files(params):
    raw_folder = params["raw_file"]
    old_folder = params["old_file"]
    
    if not os.path.exists(old_folder):
        os.makedirs(old_folder)

    for filename in os.listdir(raw_folder):
        source_file = os.path.join(raw_folder, filename)
        destination_file = os.path.join(old_folder, filename)

        # Copy each file
        if os.path.isfile(source_file):
            shutil.copy(source_file, destination_file)
            print(f"Copied: {source_file} to {destination_file}")

params = {
    "raw_file": r"D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\06_RAW_FILE\SOH\Topcare",
    "old_file": r"D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\06_RAW_FILE\SOH\Topcare\backup"
}

copy_all_files(params)
 

# Delete all Excel files in the folder
for file in file_list:
    file_path = os.path.join(path, file)
    os.remove(file_path)


print(f"Insert to {target_table} completed")

   





