import os
import pandas as pd
from sqlalchemy import create_engine
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
public_config_dir = os.path.abspath(os.path.join(script_dir, "..", "..",)) # Two level up 
sys.path.append(public_config_dir)
from public_configs.paramter_sql import local_db1


folder_path = r'C:\11_Python\01_project_soh\data\input\PWBUSSMERCH\\'

# List all Excel files in the folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xls')]

# Database connection details
db_url = local_db1['conn']
engine = create_engine(db_url)

# Query existing records from the database
existing_data_query = "SELECT * FROM pwb_uss_soh"
existing_data = pd.read_sql(existing_data_query, engine)

# Create an empty list to store the dataframes
dataframes = []

# Loop through the list of files and read each one into a dataframe
for file in excel_files:
    file_path = os.path.join(folder_path, file)

    print(file)
    if file_path is None:
        print("File path is None")
        continue  # Skip this file

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        continue  # Skip this file

    if os.path.getsize(file_path) == 0:
        print(f"File is empty (0KB): {file_path}")
        continue

    # Read the .xls file
    df = pd.read_excel(file_path)

    # Append the dataframe to the list
    dataframes.append(df)

# Combine all dataframes into one
df1 = pd.concat(dataframes, ignore_index=True)

    
# Convert column names to lowercase
df1.columns = df1.columns.str.lower()

#filter soh <> 0 
df1 = df1[df1['quant'] != 0]   

#change format type
df1['stmerch'] = df1['stmerch'].astype(str).str.zfill(5)
df1['asdate'] = df1['asdate'].astype(str)

# Remove rows already in the database
df2 = pd.concat([df1, existing_data]).drop_duplicates(keep=False)

# Insert new data into the 'sspwds_soh' table
if not df2.empty: #new_data
    df2.to_sql('pwb_uss_soh', engine, if_exists='append', index=False)
    df2.to_csv(r'C:\11_Python\01_project_soh\data\output\pwb_uss.csv', index = False)
    print("New data successfully inserted into 'pwb_uss_soh'.")
else:
    print("No new data to insert.")

# Delete all Excel files in the folder
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    os.remove(file_path)

print("All files in the folder have been deleted.")
