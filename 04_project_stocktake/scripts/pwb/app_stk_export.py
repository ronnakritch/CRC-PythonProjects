import pandas as pd
from sqlalchemy import create_engine

# Path to your Excel file
file_path = r'D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\06_RAW_FILE\STK\pwb\PWB_STK_APP2.xlsx'

# Load the data from both sheets
df_stk1 = pd.read_excel(file_path, sheet_name='STK1', usecols="A:W", dtype=str)
df_stk1.columns = df_stk1.columns.str.lower()

df_stk2 = pd.read_excel(file_path, sheet_name='STK2', usecols="A:W", dtype=str)
df_stk2.columns = df_stk2.columns.str.lower()

# Combine the two DataFrames
df_combined = pd.concat([df_stk1, df_stk2], ignore_index=True)

print(df_combined.head())

target_table = 'pwb_stk'
db_url = 'postgresql+psycopg2://chironnakrit:20309925@103.22.182.82:5432/pstdb'
engine = create_engine(db_url)

output_csv = r'C:\11_Python\log\last_update_stk.csv'
df_combined.to_sql(target_table, engine, if_exists='append', index=False)
# Save the filtered rows to a CSV file for logging
df_combined.to_csv(output_csv, index=False)

print(f"Insert to {target_table} completed")

