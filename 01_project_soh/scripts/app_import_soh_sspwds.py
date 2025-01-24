import os
import pandas as pd
from sqlalchemy import create_engine
import sys
import os
# Dynamically add the project root to the module search path
script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
public_config_dir = os.path.abspath(os.path.join(script_dir, "..", "..",)) # Two level up 
sys.path.append(public_config_dir)
from public_configs.paramter_sql import local_db1
# Specify the folder containing the Excel files
folder_path = r'C:\11_Python\01_project_soh\data\input\SSPWDS\\'

# List all Excel files in the folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xls')]

# Database connection details
db_url = local_db1['conn']
engine = create_engine(db_url)

# Query existing records from the database
existing_data_query = "SELECT * FROM sspwds_soh"
existing_data = pd.read_sql(existing_data_query, engine)

# Create an empty list to store the dataframes
dataframes = []

# Loop through the list of files and read each one into a dataframe
for file in excel_files:
    file_path = os.path.join(folder_path, file)

    print(file)
    if file_path is None:
        print("File path is None")
        continue  # Skip this file

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        continue  # Skip this file

    if os.path.getsize(file_path) == 0:
        print(f"File is empty (0KB): {file_path}")
        continue

    # Read the .xls file
    df = pd.read_excel(file_path)

    # Append the dataframe to the list
    dataframes.append(df)

# Combine all dataframes into one
df1 = pd.concat(dataframes, ignore_index=True)

# Dictionary to map old column names to new column names
column_mapping = {
    'รหัสกลุ่มลูกค้า': 'groupcuscode',
    'ชื่อกลุ่มลูกค้า': 'groupcuname',
    'รหัสลูกค้า': 'cuscode',
    'ชื่อลูกค้า': 'cusname',
    'ชื่อสั้นลูกค้า': 'cusssname',
    'SKU': 'sku',
    'Barcode IBC': 'barcodeibc',
    'Barcode SBC': 'barcodesbc',
    'ชื่อสินค้า': 'description',
    'ยี่ห้อ': 'brand',
    'รุ่น': 'model',
    'สี': 'colour',
    'ขนาด': 'size',
    'Stock': 'soh',
    'จำนวนคงค้างออก Pre-order CN': 'preordercn',
    'ราคาปกติ': 'retail',
    'ราคา Promotion': 'retailpromotion',
    'GP ปกติ': 'gp',
    'GP Promotion': 'gppromotion',
    'ราคาทุนต่อหน่วย': 'cost',
    'รหัส Dept': 'dept',
    'ชื่อ Dept': 'deptname',
    'รหัส Sub Dept': 'sdept',
    'ชื่อ Sub Dept': 'sdeptname',
    'รหัส Class': 'class',
    'ชื่อ Class': 'classname',
    'รหัส Sub Class': 'sclass',
    'ชื่อ Sub Class': 'sclassname',
    'วันที่แสดงข้อมูล': 'data_date'
}

# Rename the columns in the dataframe
df1.rename(columns=column_mapping, inplace=True)

# Remove rows already in the database
new_data = pd.concat([df1, existing_data]).drop_duplicates(keep=False)

# Insert new data into the 'sspwds_soh' table
if not new_data.empty:
    new_data.to_sql('sspwds_soh', engine, if_exists='append', index=False)
    print("New data successfully inserted into 'sspwds_soh'.")
else:
    print("No new data to insert.")

# Delete all Excel files in the folder
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    os.remove(file_path)

print("All files in the folder have been deleted.")
