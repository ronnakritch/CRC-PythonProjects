from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Assuming you have already created an engine
engine = create_engine('postgresql+psycopg2://chironnakrit:20309925@103.22.182.82:5432/pstdb')

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