import pandas as pd
import shutil
import os
 
# Load the Excel file containing the paths
file_path = r'D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\06_RAW_FILE\STK\ofm\OFM_STK_APP.xlsx'

# Load the sheets into DataFrames
df_checklist = pd.read_excel(file_path, sheet_name='checklist')
df_report1 = pd.read_excel(file_path, sheet_name='report1_stk1')
df_report3 = pd.read_excel(file_path, sheet_name='report3_credit')
 
# List of DataFrames to loop through
dataframes = [df_report1]#df_checklist, df_report3_credit, df_report1
 
# Iterate over each DataFrame
for df in dataframes:
    # Iterate over the rows in the current DataFrame
    for index, row in df.iterrows():
        source = row['path_a']
        destination = row['path_b']
 
        try:
            # Check if source exists
            if os.path.exists(source):
                
                # Create the destination directory if it doesn't exist
                destination_dir = os.path.dirname(destination)
                os.makedirs(destination_dir, exist_ok=True)
                # Copy the file
                shutil.copy(source, destination)
                print(f"Successfully copied {source} to {destination}")

            else:
                print(f"Source file does not exist: {source}")
 
        except Exception as e:
            print(f"Failed to copy {source} to {destination}: {e}")
 
