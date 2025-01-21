import pandas as pd
from sqlalchemy import create_engine,text

# Define the target SQL table name
target_table = 'chg_soh'
# Database connection string
db_url = 'postgresql+psycopg2://chironnakrit:20309925@10.2.8.118:5432/TPST'
# Create the engine to connect to PostgreSQL
engine = create_engine(db_url)

# CSV file path
csv_file_path = r'C:\11_Python\CHG.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path,encoding ='cp874')
#df = df.iloc[:11]
df = df.applymap(lambda x: x.lstrip("'") if isinstance(x, str) else x)
df = df[df['MSSTOH'] != 0]
df.columns = df.columns.str.lower()

# Output the filtered DataFrame to a CSV file
output_csv = r'C:\11_Python\CHG_cvt.csv'
df.to_csv(output_csv, index=False)
print (df)


df.to_sql(target_table, engine, if_exists='append', index=False)
print (print(f"Insert to {target_table} completed"))


