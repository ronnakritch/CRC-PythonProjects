import pandas as pd
import shutil
import os
 
#get source from STk_APP
file_path = r'D:\Users\chironnakrit\OneDrive - Central Group\เดสก์ท็อป\Works\06_RAW_FILE\STK\ofm\OFM_STK_APP.xlsx'
df_var1 = pd.read_excel(file_path, sheet_name='report1_var1')
dataframes = [df_var1]

def find_file_with_fallback(directory, filename):

    # Construct the full path
    original_path = os.path.join(directory, filename)
    
    if os.path.exists(original_path):
        return original_path
    
    else : 
        
        alt_filename1 = filename.replace(" ", "_")
        alt_path1 = os.path.join(directory, alt_filename1)
        
        if os.path.exists(alt_path1):
            print(f"file {alt_filename1} was found.")
            return alt_path1
        
        else:
            alt_filename2 = filename.replace("Credit", "CREDIT") 
            alt_path2 = os.path.join(directory, alt_filename2)
            
            if os.path.exists(alt_path2):
                print(f"file {alt_filename2} was found.")
                return alt_path2
            
            else:
                alt_filename3 = filename.replace("Credit", "CREDIT").replace(" ", "_")
                alt_path3 = os.path.join(directory, alt_filename3)

                if os.path.exists(alt_path3):
                    print(f"file {alt_filename3} was found.")
                    return alt_path3
                
                else:
                    alt_filename4 = filename.replace("Credit", "CREDIT").replace(" ", "_").replace("_20", "_")
                    alt_path4 = os.path.join(directory, alt_filename4)

                    if os.path.exists(alt_path4):
                        print(f"file {alt_filename4} was found.")
                        return alt_path4
                    else:
                        print(f"Neither {filename} not found.")
                        return None
    

def save_as_xlsx(source, destination):
    try:
        df = pd.read_excel(source)
        
        destination_dir = os.path.dirname(destination)
        os.makedirs(destination_dir, exist_ok=True)

        destination = destination.replace('.xls', '.xlsx')  
        df.to_excel(destination, index=False)
        print(f"Successfully saved {destination}")
        
    except Exception as e:
        print(f"Failed to save {source} : {e}") 

for df in dataframes:
    
    for index, row in df.iterrows():
        path_source = row['from']
        credit_filename = row['filename_credit']
        credit_destination = row['path_dest_credit']

        # Process credit file
        found_credit_source = find_file_with_fallback(path_source,credit_filename)
        if found_credit_source and found_credit_source.endswith('.xls'):
            save_as_xlsx(found_credit_source, credit_destination)
        else:
            print(f"Credit source not found: {credit_filename}")

 
