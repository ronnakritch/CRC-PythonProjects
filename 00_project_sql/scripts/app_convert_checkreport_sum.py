from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
# Project root (one level up)
project_root = os.path.abspath(os.path.join(script_dir, ".."))
# Public config directory (two levels up)
public_config_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(project_root)
sys.path.append(public_config_dir)

from public_configs.paramter_sql import cloud_db1
engine = create_engine(cloud_db1['conn'])

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Define the query to fetch data
query = text("""
SELECT 
    *
FROM 
    temp_check_report_summary
WHERE
    cntdate >= '2024-01-01'
""")

# Execute the query and fetch all results
result = session.execute(query)
data = result.fetchall()

# Delete existing rows for the specified condition
delete_query = text("""
DELETE FROM check_report_summary
""")
session.execute(delete_query)

# Insert all the fetched data into the table
table = 'check_report_summary'
filtered_df1.to_sql(table, engine, if_exists='append', index=False)

# Commit the transaction
session.commit()

# Close the session
session.close()
