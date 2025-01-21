import pandas as pd
from sqlalchemy import create_engine, text

# Define the target SQL table name
target_table = 'checklist'
source_view = 'temp_check_report_summary'
db_url = 'postgresql+psycopg2://chironnakrit:20309925@103.22.182.82:5432/pstdb'
engine = create_engine(db_url)

file_path = r"D:\Users\chironnakrit\Desktop\temp_check_report_summary_202412261622.csv"
output_path = r"D:\Users\chironnakrit\Desktop\check_report_unpivoted.csv"

# Load the data
data = pd.read_csv(file_path)

# Identifying columns to unpivot
columns_to_unpivot = [col for col in data.columns if col not in ['bu', 'stcode', 'cntdate', 'type1', 'atype']]

# Columns to retain as identifiers
id_cols = ['bu', 'stcode', 'cntdate', 'type1', 'atype']

# Unpivot the columns
unpivoted_data = pd.melt(
    data,
    id_vars=id_cols,
    value_vars=columns_to_unpivot,
    var_name='file_type',
    value_name='value'
)

# Replace values in the 'value' column
unpivoted_data['status'] = unpivoted_data['value'].replace({'Pass': 'Y', 'Not Pass': 'Y'}).fillna('N')

# Save the unpivoted data to a CSV file
unpivoted_data.to_csv(output_path, index=False)

print(f"Unpivoted data has been saved to {output_path}")
