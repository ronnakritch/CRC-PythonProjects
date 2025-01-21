import pandas as pd
import shutil
import os
 
# Load the Excel file containing the paths
file_path = r'D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\08_PQ\Missrate\Missrate_update.xlsx'

# Load the sheets into DataFrames
df_missrate = pd.read_excel(file_path, sheet_name='Missrate_update')
 
# List of DataFrames to loop through
dfs = [df_missrate]
 
for df in dfs:
    # Iterate over the rows in the current DataFrame
    for index, row in df.iterrows():
        source = row['source_path']
        destination = row['dest_path']

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