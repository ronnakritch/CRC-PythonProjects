import pandas as pd
from sqlalchemy import create_engine,text
from datetime import datetime, timezone, timedelta

# Output CSV file path
output_file_path = r'D:\Users\chironnakrit\Central Group\PST Performance Team - Documents\Apps\soh_update_raw.csv'

# Define the target SQL table name
source_table = 'soh_update_v2'
# Database connection string
db_url = 'postgresql+psycopg2://chironnakrit:20309925@AUDCRCHA0020015/pstdb2'
# Create the engine to connect to PostgreSQL
engine = create_engine(db_url)
    
utc_dt = datetime.now(timezone.utc) - timedelta(days=15) 
formatted_date = utc_dt.strftime("%Y%m%d")
print (f"data form {formatted_date} to now")

# SQL query to select all data from the view
with engine.connect() as connection:
    result = connection.execute(text(f"SELECT * FROM {source_table} where data_date::numeric > {formatted_date}" ))
    df = pd.DataFrame(result.fetchall(), columns=result.keys())

# Export DataFrame to CSV
df.to_csv(output_file_path, index=False)

print(f"Data exported successfully to {output_file_path}")










