import pandas as pd
import kagglehub
import sqlite3
import os

#! Read each function through Grok and generate a DOC STRING describing what
#! each one does

def import_sql_script(sql_script_path):
    
    with open(sql_script_path, 'r') as sql_file_wrapper:
        sql_file = sql_file_wrapper.read()

    return sql_file


def pull_kaggle_data(kaggle_path = "syedanwarafridi/vehicle-sales-data",
                     file_path_suffix = "/car_prices.csv"):

    stored_file_path = kagglehub.dataset_download(kaggle_path)
    file_path = stored_file_path + file_path_suffix
    df = pd.read_csv(file_path)

    return df


def get_sql_column_datatypes(df):

    str_dtypes = df.dtypes.astype(str)
    str_dtypes = str_dtypes.str.replace("int64", 'int')
    str_dtypes = str_dtypes.str.replace("float64", 'float')
    str_dtypes = str_dtypes.str.replace("object", 'text')

    return str_dtypes


def get_create_sql_table_command(df, 
                             table_name = 'vehicle_sales_data',
                             primary_key_columns = ['vin', 'saledate', 'sellingprice', 'odometer']):

    df_str_dtypes = get_sql_column_datatypes(df = df)

    #! For loop right now, could be a LIST COMPREHENSION
    data_type_str = ""
    for col_name, col_type in df_str_dtypes.to_dict().items():
        data_type_str = data_type_str + f"{col_name} {col_type}, "
    
    data_type_str = data_type_str[:-2]

    primary_key_col_str = ", ".join(primary_key_columns)
    
    create_table_command = f"""CREATE TABLE IF NOT EXISTS
        {table_name}({data_type_str},
            PRIMARY KEY ({primary_key_col_str}))"""
    
    return create_table_command


def get_sql_insert_commands(df,
                        table_name):
    
    insert_commands = []
    for _, row in df.iterrows():
        # _, row = list(df.iterrows())[0]
        
        #! If numpy.float is in the string of element's TYPE, then convert it
        #! to a normal Python float. Otherwise, do nothing
        adjusted_row_values = [float(elem)
                                if 'numpy.float' in str(type(elem)) 
                                else elem 
                                for elem in row.values]

        iter_insert_str = f"INSERT OR IGNORE INTO {table_name} VALUES {tuple(adjusted_row_values)}"
        iter_insert_str = iter_insert_str.replace(" nan,", " NULL,"
                                        ).replace(" nan)", " NULL)")

        insert_commands.append(iter_insert_str)

    return insert_commands


class SQLiteDataObject:

    def __init__(self, database_name = "tool_data"):
        # from types import SimpleNamespace; self = SimpleNamespace()
        
        self.database_name = database_name
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
    def create_sqlite_conn(self):
        
        db_path = f"{self.base_dir}/{self.database_name}.db"
        conn = sqlite3.connect(db_path)

        return conn
    
    def execute_sqlite_commands(self,
                                commands):

        with self.create_sqlite_conn() as conn:
            cursor = conn.cursor()
            for command in commands:
                cursor.execute(command)

    def query_from_database(self, query):
        
        with self.create_sqlite_conn() as conn:
            
            cursor         = conn.cursor()
            raw_sql_output = cursor.execute(query)
            row_values     = cursor.fetchall()

        column_values = [_description[0] for _description in raw_sql_output.description]
        df = pd.DataFrame(data = row_values,
                          columns = column_values)
        
        return df
