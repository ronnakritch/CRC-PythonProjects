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
filtered_df1.to_sql(table, engine, if_exists='append', index=False)

# Commit the transaction
session.commit()

# Close the session
session.close()
