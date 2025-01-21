import pandas as pd
import shutil
import os
 
# Load the Excel file containing the paths
file_path = r'D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\08_PQ\path_data_all2.xlsx'
 
# Load the 'report1' sheet into a DataFrame
df_report1 = pd.read_excel(file_path, sheet_name='fileall')
 
# Iterate over the rows in df_report1
for index, row in df_report1.iterrows():
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
 
print('End of file copied')
 