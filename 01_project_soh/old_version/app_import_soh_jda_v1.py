import pandas as pd
import psycopg2
import csv
import os
from parameter_soh_jda import OFM_parameter , B2S_parameter, SSP_parameter

# List of parameter sets
parameter_sets = [OFM_parameter]#, B2S_parameter]#[SSP_parameter]# 

for params in parameter_sets:
    # Check if the file exists
    if not os.path.exists(params["raw_file"]):
        print(f"Error: The file '{params['raw_file']}' does not exist.")
        continue
    
    try:
        # Get Column name from soh_parameter
        column_names = params["col_name"]

        # เปลี่ยนชื่อคอลัมน์เป็นตัวพิมพ์เล็ก
        lowercase_columns = [col.lower() for col in column_names]

        # โหลดข้อมูลเข้ามาและกำหนดชื่อคอลัมน์เป็นตัวพิมพ์เล็ก
        df = pd.read_csv(params["raw_file"], header=None, names=lowercase_columns, encoding='ISO-8859-1')
        #df = pd.read_csv(params["raw_file"], header=None, names=lowercase_columns, encoding='ISO-8859-1', engine='python')
        
        # Export DataFrame เป็นไฟล์ CSV
        df.to_csv(params["convert_file"], index=False)
        print(f"Convert The file CSV '{params['convert_file']}' completed.")
    
    except Exception as e:
        print(f"Error reading or processing Excel file: {e}")
        continue  # ถ้าเกิดข้อผิดพลาด, ข้ามไปยัง parameter set ถัดไป

    # Database connection parameters
    database = "pst2"
    user = "chironnakrit"
    password = "20309925"
    host = "141.98.17.88"
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

        # Insert data into the database
        try:
            with open(params["convert_file"], 'r', encoding='ISO-8859-1') as f:
                reader = csv.reader(f)
                header = next(reader)  # Read the header row

                # Create SQL INSERT statement dynamically using the column names
                columns = ', '.join(header)
                placeholders = ', '.join(['%s'] * len(header))
                insert_sql = f'''
                INSERT INTO {params["sql_table"]}
                ({columns})
                VALUES ({placeholders})
                '''

                for row in reader:
                    cursor.execute(insert_sql, row)

            conn.commit()  # Commit the transaction
            print(f"Data '{params['convert_file']}' inserted successfully.")

        except Exception as e:
            conn.rollback()  # Rollback the transaction on error
            print(f"Error inserting data: {e}")
        
        finally:
            cursor.close()
            conn.close()

    except Exception as e:
        print(f"Error connecting to the database: {e}")

