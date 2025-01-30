import pandas as pd
from sqlalchemy import create_engine, text

import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
public_config_dir = os.path.abspath(os.path.join(script_dir, "..", "..",))
sys.path.append(public_config_dir)

from public_configs.paramter_sql import cloud_db1

target_table = 'soh_update_pwb_3q'
db_url = cloud_db1['conn']
engine = create_engine(db_url)

csv_file_path = r'D:\Users\chironnakrit\Central Group\PST Performance Team - Documents\Apps\soh_update_pwb_3q_raw.csv'

df = pd.read_csv(csv_file_path)
df['data_date'] = df['data_date'].astype(str)

with engine.connect() as connection:
    result = connection.execute(text(f'SELECT code, "DATE" FROM {target_table}'))
    dtf = pd.DataFrame(result.fetchall(), columns=result.keys())
dtf['DATE'] = dtf['DATE'].astype(str)

merged_df = pd.merge(df, dtf, how='left', left_on=['code', 'data_date'], right_on=['code', 'DATE'], suffixes=('_csv', '_sql'))
filtered_df1 = merged_df[merged_df['DATE'].isnull()]
print(filtered_df1)

keepcolumn = ['code', 'bu', 'store_code', 'data_date', 'atype',
    'food_credit', 'nonfood_consign', 
    'perishable_nonmer', 'totalsoh'
]
filtered_df2 = filtered_df1[keepcolumn]

new_column_names = [
    'code', 'bu', 'stcode', 'DATE', 'atype',
    'food_credit', 'nonfood_consign', 
    'perishable_nonmer', 'totalsoh'
]
filtered_df2.columns = new_column_names
filtered_df2['stcode'] = filtered_df2['stcode'].astype(str).str.zfill(5)
print(filtered_df2)

output_csv = r'C:\11_Python\01_project_soh\log\last_soh_update_pwb_3q.csv'
filtered_df2.to_csv(output_csv, index=False)
print(f"Filtered and renamed data has been saved to: {output_csv} completed")

filtered_df2.to_sql(target_table, engine, if_exists='append', index=False)
print(f"Insert to {target_table} completed")
