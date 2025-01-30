import pandas as pd
from sqlalchemy import create_engine,text
from datetime import datetime, timezone, timedelta
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"script_dir: {script_dir}")
public_config_dir = os.path.abspath(os.path.join(script_dir, "..", "..",))
sys.path.append(public_config_dir)
try:
    from public_configs.paramter_sql import local_db1
except ModuleNotFoundError as e:
    print(f"Error: {e}")
    print(f"public_config_dir: {public_config_dir}")
    raise

output_file_path = r'D:\Users\chironnakrit\Central Group\PST Performance Team - Documents\Apps\soh_update_pwb_3q_raw.csv'

source_table = 'soh_update_pwb_3q'
db_url = local_db1['conn']
engine = create_engine(db_url)
    
utc_dt = datetime.now(timezone.utc) - timedelta(days=15) 
formatted_date = utc_dt.strftime("%Y%m%d")
print (f"data form {formatted_date} to now")

with engine.connect() as connection:
    result = connection.execute(text(f"SELECT * FROM {source_table} where data_date::numeric > {formatted_date}" ))
    df = pd.DataFrame(result.fetchall(), columns=result.keys())

df.to_csv(output_file_path, index=False)

print(f"Data exported successfully to {output_file_path}")










