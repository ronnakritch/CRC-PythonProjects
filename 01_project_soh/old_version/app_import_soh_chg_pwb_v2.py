import pandas as pd
from sqlalchemy import create_engine
from parameter_soh_chg_pwb import CHG_parameter, PWB_parameter
from sqlalchemy import create_engine, text

# Define the target SQL
db_url = 'postgresql+psycopg2://chironnakrit:20309925@AUDCRCHA0020015/pstdb2' #เปลี่ยนชั่วคราว
engine = create_engine(db_url)

# List of parameter sets
parameter_sets = [PWB_parameter, CHG_parameter]

for params in parameter_sets:

    df = pd.read_csv(params["raw_file"], encoding='cp874')
    df = df.applymap(lambda x: x.lstrip("'") if isinstance(x, str) else x)
    df = df[df[params["soh_col"]] != 0]
    
    # Convert column names to lowercase
    df.columns = df.columns.str.lower()
    
    #change format type
    df['msstor'] = df['msstor'].astype(str)
    df['msasdt'] = df['msasdt'].astype(str)

    with engine.connect() as connection:
        result = connection.execute(text(f'SELECT msstor, msasdt FROM {params['sql_table']}'))
        dfs = pd.DataFrame(result.fetchall(), columns=result.keys())

    #change format type
    dfs['msstor'] = dfs['msstor'].astype(str)
    dfs['msasdt'] = dfs['msasdt'].astype(str)

    # Perform a left join between the Excel DataFrame and the SQL DataFrame
    #merged_df = df.merge(dfs, how='left', on=['msstor', 'msasdt'], indicator=True) 

    # Filter rows that are only in the Excel file (not in the database)
    #filtered_df = merged_df[merged_df['_merge'] == 'left_only']

    # Output the filtered DataFrame to a CSV file
    output_csv = params["convert_file"]
    #filtered_df.to_csv(output_csv, index=False)
    df.to_csv(output_csv, index=False)#เปลี่ยนชั่วคราว

    # Insert the data into the SQL table
    target_table = params["sql_table"]
    #filtered_df.to_sql(target_table, engine, if_exists='append', index=False)
    #df.to_sql(target_table, engine, if_exists='append', index=False)#เปลี่ยนชั่วคราว

    print(f"Insert to {target_table} completed")






