import pandas as pd
from sqlalchemy import create_engine, text

# Path to your Excel file
file_path = r'D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\06_RAW_FILE\STK\pwb\PWB_STK_APP2.xlsx'

# Load the data from both sheets
df_var1 = pd.read_excel(file_path, sheet_name='VAR1', usecols="A:R", dtype=str)
df_var1.columns = df_var1.columns.str.lower()
df_var1= df_var1.rename(columns={'location': 'LOCATION'})

df_var2 = pd.read_excel(file_path, sheet_name='VAR2', usecols="A:R", dtype=str)
df_var2.columns = df_var2.columns.str.lower()
df_var2 = df_var2.rename(columns={'location': 'LOCATION'})

# Combine the two DataFrames
df_combined = pd.concat([df_var1, df_var2], ignore_index=True)
#df_combined = df_var2
print(df_combined.head())

target_table = 'pwb_var'
db_url = 'postgresql+psycopg2://chironnakrit:20309925@103.22.182.82:5432/pstdb'
engine = create_engine(db_url)

df_combined.to_sql(target_table, engine, if_exists='append', index=False)
output_csv = r'C:\11_Python\log\last_update_var.csv'
df_combined.to_csv(output_csv, index=False)

print(f"Insert to {target_table} completed")

