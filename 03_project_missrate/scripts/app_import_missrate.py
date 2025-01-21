import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine,text
import shutil
 
# Specify the folder containing the Excel files
f_path = r'D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\08_PQ\Missrate\raw_file'
error_path = r'D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\08_PQ\Missrate\error_file'
e_path= r'D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\08_PQ\Missrate\backup_file'
table = 'missrate'
 
# List all Excel files in the folder
excel_files = [f for f in os.listdir(f_path) if f.endswith('.xlsx')]
 
# Create an empty list to store the dataframes
dataframes = []
 
for file in excel_files:
    print(file)
    file_path = os.path.join(f_path, file)
    
    # Read the desired sheet and columns from 'Summary'
    df = pd.read_excel(file_path, sheet_name='Summary', usecols='A:J', skiprows=range(1, 6), header=1 , dtype=str)

    #filter barcode is null
    df = df[df['Barcode'].notnull()]

    # Check if either 'PST/Store' or 'PST/Outsource' exists
    if 'PST/Store' in df.columns:
        pst_column = 'PST/Store'
    elif 'PST/Outsource' in df.columns:
        pst_column = 'PST/Outsource'
        # Rename 'PST/Outsource' to 'PST/Store' for consistency
        df = df.rename(columns={'PST/Outsource': 'PST/Store'})
    else:
        # If neither column exists, move the file to the error folder and skip
        error_file_path = os.path.join(error_path, file)
        shutil.copy(file_path, error_file_path)
        print(f"Error: Neither 'PST/Store' nor 'PST/Outsource' column found in {file}. File moved to error folder.")
        continue

    # Check if the 'PST/Store' column is null or doesn't exist
    if  df['PST/Store'].isnull().any():
        error_file_path = os.path.join(error_path, file)
        shutil.move(file_path, error_file_path)
        print(f"Error:'PST/Store' column  empty in {file}. File moved to error folder.")
        continue 
    
    #convert outsource name to "Outsource"
    df.loc[df['PST/Store'].str.lower().isin(['ajis', 'pcs', 'smollan','ssd']), 'PST/Store'] = 'Outsource'

    #Scan error calculate
    df = df.drop(columns=['Scan Error'])
    df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
    df['Add/Edit'] = pd.to_numeric(df['Add/Edit'], errors='coerce')
    
    # Apply conditional logic
    df['Scan Error'] = np.where(df['Remark (Root Cause)'] != 'แก้ไข Edition ผิด', 
                            abs(df['Count'] - df['Add/Edit']), 
                            '0')

    # Check for duplicates
    if df.duplicated().any():
        # Copy the file to the error folder and skip processing
        error_file_path = os.path.join(error_path, file)
        shutil.copy(file_path, error_file_path)
        print(f"Error: Duplicates found in {file}. File moved to error folder.")
        continue

    # Read the entire sheet to search for specific text
    sheet_data = pd.read_excel(file_path, sheet_name='Summary', header=None , dtype=str)
    
    # Find the row and column of the required keywords
    def find_cell_value(keyword, sheet_data, offset_right_pst, offset_right_outsource):
        cell_location = sheet_data[sheet_data.isin([keyword])].stack().index.tolist()
        if cell_location:
            row, col = cell_location[0]
            value_pst = sheet_data.iloc[row, col + offset_right_pst]
            value_outsource = sheet_data.iloc[row, col + offset_right_outsource]
            # Replace None or NaN with 0
            value_pst = value_pst if pd.notnull(value_pst) else 0
            value_outsource = value_outsource if pd.notnull(value_outsource) else 0
            return value_pst, value_outsource
        else:
            return 0, 0
    
    # Get values for "All Scan", "Qty weight", and "SKU weright"
    all_scan_pst, all_scan_outsource = find_cell_value("All Scan", sheet_data, offset_right_pst=1, offset_right_outsource=2)
    qty_weight_pst, qty_weight_outsource = find_cell_value("Qty weight", sheet_data, offset_right_pst=1, offset_right_outsource=2)
    sku_weight_pst, sku_weight_outsource = find_cell_value("SKU weright", sheet_data, offset_right_pst=1, offset_right_outsource=2)
    
    # Extract parts of the filename to create new columns (cols1, cols2, cols3, cols4)
    file_parts = os.path.splitext(file)[0].split('_')
    
    # Ensure the filename has enough parts
    if len(file_parts) == 4:
        cols1, cols2, cols3, cols4 = file_parts
    else:
        # Handle cases where the filename format is unexpected
        cols1, cols2, cols3, cols4 = None, None, None, None

    # Add new columns to the dataframe
    df['bu'] = cols2
    df['stcode'] = cols3
    df['cntdate'] = cols4
    
    # Add the new columns based on the found cell values
    df['all scan-pst'] = all_scan_pst
    df['qty weight-pst'] = qty_weight_pst
    df['sku weright-pst'] = sku_weight_pst
    df['all scan-outsource'] = all_scan_outsource
    df['qty weight-outsource'] = qty_weight_outsource
    df['sku weright-outsource'] = sku_weight_outsource

    # Append the dataframe to the list
    dataframes.append(df)
 
# Combine all dataframes into one
df1 = pd.concat(dataframes, ignore_index=True)
df1.columns = df1.columns.str.lower()
print(df1)
df_file = r'D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\08_PQ\Missrate\Missrate_dfcheck.csv'
df1.to_csv(df_file, index=False)

# Define the column names to keep
keepcol = [
    'group', 'department', 'barcode',
    'name',
    'count',
    'add/edit',
    'pst/store',
    'remark (root cause)',
    'note',
    'scan error',
    'bu',
    'stcode',
    'cntdate',
    'all scan-pst',
    'qty weight-pst',
    'sku weright-pst',  
    'all scan-outsource',
    'qty weight-outsource',
    'sku weright-outsource'  
]

df1 = df1[keepcol]


new_column_names = [
'group', 'department', 'barcode', 'name', 'count', 'add/edit',
'pst/store', 'remark root cause', 'note', 'scan error', 'bu',
'stcode', 'cntdate', 'all scan-pst', 'qty weight-pst',
'sku weright-pst', 'all scan-outsource', 'qty weight-outsource',
'sku weright-outsource'
]

df1.columns = new_column_names

# Save the dataframe to a CSV file
csv_file_path = r'D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\08_PQ\Missrate\missrate_check.csv'
df1.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
print(f"CSV file saved at {csv_file_path} successed.")
 
# PostgreSQL connection details
db_url = 'postgresql+psycopg2://prthanapat:20020015@103.22.182.82:5432/pstdb' 
engine = create_engine(db_url)

user_input = input("Do you want to insert data into the database? (y/n): ").strip().lower()
 
if user_input == 'y':
    
    # Connect to the first database and retrieve existing data
    with engine.connect() as connection:
        result = connection.execute(text(f'SELECT stcode, cntdate, barcode FROM {table}'))
        dfs = pd.DataFrame(result.fetchall(), columns=result.keys())

    # Convert 'stcode', 'cntdate', and 'barcode' columns to string in the SQL DataFrame
    dfs['stcode'] = dfs['stcode'].astype(str)
    dfs['cntdate'] = dfs['cntdate'].astype(str)
    dfs['barcode'] = dfs['barcode'].astype(str)

    # Perform a left join between the Excel DataFrame and the SQL DataFrame
    merged_df1 = df1.merge(dfs, how='left', on=['stcode', 'cntdate', 'barcode'], indicator=True)

    # Filter rows that are only in the Excel file (not in the database)
    filtered_df1 = merged_df1[merged_df1['_merge'] == 'left_only']

    # Save the filtered rows to CSV files
    csv_file1 = r'D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\08_PQ\Missrate\Missrate_filtered_data_pstdb.csv'
    filtered_df1.to_csv(csv_file1, index=False)

    # Insert the data into the first and second databases
    filtered_df1.drop(columns=['_merge'], inplace=True)
    filtered_df1.to_sql(table, engine, if_exists='append', index=False)
    
    print("Data successfully inserted into " + table)

    # Delete all files in the destination folder
    for filename in os.listdir(e_path):
        file_path = os.path.join(e_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    # Move all files from source to destination
    for filename in os.listdir(f_path):
        source_file = os.path.join(f_path, filename)
        destination_file = os.path.join(e_path, filename)
        print("Raw files had moved to backup folder.")
    # Check if it's a file (not a directory)
        if os.path.isfile(source_file):
            shutil.move(source_file, destination_file)
        else : print("f_path not files")

    print("Process completed.")    
else:
    print("Data insertion aborted.")