from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
# Project root (one level up)
project_root = os.path.abspath(os.path.join(script_dir, ".."))
# Public config directory (two levels up)
public_config_dir = os.path.abspath(os.path.join(script_dir, "..", "..",))
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
    temp_check_report_cntfile
where
    cntdate >= '2024-01-01'
""")

# Execute the query
result = session.execute(query)

# Fetch all results
data = result.fetchall()

# Insert or update data in the target table
for row in data:
    bu, stcode, branch, shub, type1, cntdate, status = row
    check_query = text("""
    SELECT 1 FROM check_report_cntfile
    WHERE bu = :bu AND stcode = :stcode AND cntdate = :cntdate
    """)
    exists = session.execute(check_query, {'bu': bu, 'stcode': stcode, 'cntdate': cntdate}).fetchone()

    if exists:
        update_query = text("""
        UPDATE check_report_cntfile
        SET status = :status
        WHERE bu = :bu AND stcode = :stcode AND cntdate = :cntdate
        """)
        session.execute(update_query, {
            'bu': bu,
            'stcode': stcode,
            'branch': branch,
            'shub': shub,
            'type1': type1,
            'cntdate': cntdate,
            'status': status
        })
    else:
        insert_query = text("""
        INSERT INTO check_report_cntfile (bu, stcode, branch, shub, type1, cntdate, status)
        VALUES (:bu, :stcode, :branch, :shub, :type1, :cntdate, :status)
        """)
        session.execute(insert_query, {
            'bu': bu,
            'stcode': stcode,
            'branch': branch,
            'shub': shub,
            'type1': type1,
            'cntdate': cntdate,
            'status': status
        })

# Commit the transaction
session.commit()

# Close the session
session.close()