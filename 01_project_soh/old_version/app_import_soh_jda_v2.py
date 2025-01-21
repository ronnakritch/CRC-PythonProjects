import pandas as pd
import psycopg2
import shutil
from psycopg2.extras import execute_values
import os
from parameter_soh_jda import OFM_parameter, B2S_parameter, SSP_parameter


# List of parameter sets
parameter_sets = [OFM_parameter, B2S_parameter,SSP_parameter]

for params in parameter_sets:
    
    # Check if the file exists
    if not os.path.exists(params["raw_file"]):
        print(f"Error: The file '{params['raw_file']}' does not exist.")
        continue
    
    # Check if the content of the raw file and old file are the same
    if os.path.exists(params["old_file"]):
        try:
            # Read both files into DataFrames
            df_raw = pd.read_csv(params["raw_file"], encoding='cp874')
            df_old = pd.read_csv(params["old_file"], encoding='cp874')
            
            # Compare the DataFrames
            if df_raw.equals(df_old):
                print(f"No updating file detected between '{params['raw_file']}' and '{params['old_file']}'. Skipping processing.")
                continue
        except Exception as e:
            print(f"Error comparing files '{params['raw_file']}' and '{params['old_file']}': {e}")
            continue

    try:
        # Get Column name from soh_parameter
        column_names = params["col_name"]

        # เปลี่ยนชื่อคอลัมน์เป็นตัวพิมพ์เล็ก
        lowercase_columns = [col.lower() for col in column_names]

        # โหลดข้อมูลเข้ามาและกำหนดชื่อคอลัมน์เป็นตัวพิมพ์เล็ก
        df = pd.read_csv(params["raw_file"], header=None, names=lowercase_columns, encoding='cp874')

        # filter soh <> 0 
        df2 = df[df[params["soh_col"]] != 0 ] 

        # Export DataFrame เป็นไฟล์ CSV
        df.to_csv(params["convert_file"], index=False)
        print(f"Convert The file CSV '{params['convert_file']}' completed.")
    
    except Exception as e:
        print(f"Error reading or processing CSV file: {e}")
        continue  # ถ้าเกิดข้อผิดพลาด, ข้ามไปยัง parameter set ถัดไป

    # Database connection parameters
    database = "pstdb" #"TPST"
    user = "chironnakrit"
    password = "20309925"
    host = "103.22.182.82" #"TPSTSERVER"
    port = "5432"

    try:
        # Create the connection
        conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )

        cursor = conn.cursor()

        # Insert data into the database using execute_values for bulk insert
        try:
            # Prepare the insert SQL statement
            insert_sql = f'''
            INSERT INTO {params["sql_table"]}
            ({', '.join(lowercase_columns)})
            VALUES %s
            '''

            # Convert DataFrame rows to a list of tuples
            data = [tuple(row) for row in df.to_numpy()]

            # Execute the bulk insert
            execute_values(cursor, insert_sql, data)

            conn.commit()  # Commit the transaction
            print(f"Data from '{params['convert_file']}' inserted successfully into '{params['sql_table']}'.")

        except Exception as e:
            conn.rollback()  # Rollback the transaction on error
            print(f"Error inserting data: {e}")
        
        finally:
            cursor.close()
            conn.close()

        # Copy the file from the raw file path to the old file path
        shutil.copy(params["raw_file"], params["old_file"])

    except Exception as e:
        print(f"Error connecting to the database: {e}")
