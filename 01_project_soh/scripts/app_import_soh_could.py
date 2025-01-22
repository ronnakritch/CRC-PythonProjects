import pandas as pd
from sqlalchemy import create_engine, text

# Define the target SQL table name
target_table = 'soh_update'
db_url = 'postgresql+psycopg2://chironnakrit:20309925@103.22.182.82:5432/pstdb'
engine = create_engine(db_url)

csv_file_path = r'D:\Users\chironnakrit\Central Group\PST Performance Team - Documents\Apps\soh_update_raw.csv'

df = pd.read_csv(csv_file_path)

# Convert 'data_date' in df to string to match 'DATE' in dtf (if necessary)
df['data_date'] = df['data_date'].astype(str)

# Execute select from SQL
with engine.connect() as connection:
    result = connection.execute(text(f'SELECT code, "DATE" FROM {target_table}'))
    dtf = pd.DataFrame(result.fetchall(), columns=result.keys())

# Convert 'DATE' in dtf to string to match 'data_date' in df (if necessary)
dtf['DATE'] = dtf['DATE'].astype(str)

# Perform a left join between the CSV DataFrame and the SQL DataFrame
merged_df = pd.merge(df, dtf, how='left', left_on=['code', 'data_date'], right_on=['code', 'DATE'], suffixes=('_csv', '_sql'))

# Filter rows where 'DATE' from the SQL table is null (no match found)
filtered_df1 = merged_df[merged_df['DATE'].isnull()]
print(filtered_df1)

keepcolumn = ['code', 'bu', 'store_code', 'data_date', 
    'food_credit', 'nonfood_consign', 
    'perishable_nonmer', 'totalsoh'
]

filtered_df2 = filtered_df1[keepcolumn]

# Define new column names for the CSV and database insertion
new_column_names = [
    'code', 'bu', 'stcode', 'DATE', 
    'food_credit', 'nonfood_consign', 
    'perishable_nonmer', 'totalsoh'
]

# Rename the columns in filtered_df2 to match the new_column_names
filtered_df2.columns = new_column_names
print(filtered_df2)

# Output the filtered DataFrame to a CSV file
output_csv = r'C:\11_Python\01_project_soh\log\last_update_soh.csv'
filtered_df2.to_csv(output_csv, index=False)

# Print completion message
print(f"Filtered and renamed data has been saved to: {output_csv} completed")

# Insert the DataFrame into the 'soh_update' table
filtered_df2.to_sql(target_table, engine, if_exists='append', index=False)
print(f"Insert to {target_table} completed")
