import pandas as pd
import kagglehub
import sqlite3
import os

def import_sql_script(sql_script_path):
    """
    Reads and returns the contents of a SQL script file.

    Args:
        sql_script_path (str): The file path to the SQL script to be imported.

    Returns:
        str: The contents of the SQL script file as a string.

    Raises:
        FileNotFoundError: If the specified SQL script file cannot be found.
        IOError: If there's an error reading the file.
    """
    with open(sql_script_path, 'r') as sql_file_wrapper:
        sql_file = sql_file_wrapper.read()

    return sql_file


def pull_kaggle_data(kaggle_path = "syedanwarafridi/vehicle-sales-data",
                     file_path_suffix = "/car_prices.csv"):
    """
    Downloads and reads a CSV dataset from Kaggle.

    Args:
        kaggle_path (str, optional): The Kaggle dataset path in the format "username/dataset-name".
            Defaults to "syedanwarafridi/vehicle-sales-data".
        file_path_suffix (str, optional): The suffix to append to the downloaded dataset path
            to locate the specific CSV file. Defaults to "/car_prices.csv".

    Returns:
        pandas.DataFrame: A DataFrame containing the data from the CSV file.

    Raises:
        ImportError: If required libraries (kagglehub or pandas) are not installed.
        FileNotFoundError: If the specified file cannot be found after download.
        KaggleApiError: If there's an issue with the Kaggle API authentication or download.
    """
    stored_file_path = kagglehub.dataset_download(kaggle_path)
    file_path = stored_file_path + file_path_suffix
    df = pd.read_csv(file_path)

    return df


def get_sql_column_datatypes(df):
    """
    Converts pandas DataFrame column data types to SQL-compatible type names.

    Args:
        df (pandas.DataFrame): The input DataFrame whose column types need to be converted.

    Returns:
        pandas.Series: A Series containing SQL-compatible data type names indexed by column names.

    Notes:
        - Converts 'int64' to 'int'
        - Converts 'float64' to 'float'
        - Converts 'object' to 'text'
        - Other pandas data types are returned as strings without modification

    Raises:
        AttributeError: If the input is not a pandas DataFrame or lacks the dtypes attribute.
    """
    str_dtypes = df.dtypes.astype(str)
    str_dtypes = str_dtypes.str.replace("int64", 'int')
    str_dtypes = str_dtypes.str.replace("float64", 'float')
    str_dtypes = str_dtypes.str.replace("object", 'text')

    return str_dtypes


def get_create_sql_table_command(df, 
                             table_name = 'vehicle_sales_data',
                             primary_key_columns = ['vin', 'saledate', 'sellingprice', 'odometer']):
    """
    Generates a SQL CREATE TABLE command based on DataFrame column types and specified primary keys.

    Args:
        df (pandas.DataFrame): The input DataFrame to base the table structure on.
        table_name (str, optional): Name of the table to create. 
            Defaults to 'vehicle_sales_data'.
        primary_key_columns (list, optional): List of column names to use as primary keys.
            Defaults to ['vin', 'saledate', 'sellingprice', 'odometer'].

    Returns:
        str: A SQL command string to create a table with specified columns and primary keys.

    Notes:
        - Uses get_sql_column_datatypes() to convert pandas types to SQL types
        - Creates a composite primary key if multiple columns are specified
        - Includes 'IF NOT EXISTS' clause to prevent errors if table already exists

    Raises:
        AttributeError: If df is not a pandas DataFrame or lacks required attributes.
        KeyError: If any primary_key_columns are not present in the DataFrame.
    """
    df_str_dtypes = get_sql_column_datatypes(df = df)

    data_type_str = ""
    for col_name, col_type in df_str_dtypes.to_dict().items():
        data_type_str = data_type_str + f"{col_name} {col_type}, "
    
    data_type_str = data_type_str[:-2]

    primary_key_col_str = ", ".join(primary_key_columns)
    
    create_table_command = f"""CREATE TABLE IF NOT EXISTS
        {table_name}({data_type_str},
            PRIMARY KEY ({primary_key_col_str}))"""
    
    return create_table_command


def get_sql_insert_commands(df, table_name):
    """
    Generates a list of SQL INSERT commands for each row in a DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame containing data to insert.
        table_name (str): The name of the target table for insertion.

    Returns:
        list: A list of SQL INSERT command strings, one for each row in the DataFrame.

    Notes:
        - Uses 'INSERT OR IGNORE' to skip duplicate entries
        - Converts numpy.float types to Python float
        - Replaces NaN values with SQL NULL
        - Assumes column order in DataFrame matches table structure

    Raises:
        AttributeError: If df is not a pandas DataFrame or lacks required attributes.
    """
    insert_commands = []
    for _, row in df.iterrows():        

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
    """
    A class to manage SQLite database operations including connection, execution, and querying.

    Attributes:
        database_name (str): Name of the SQLite database file (without .db extension).
        base_dir (str): Absolute path to the directory containing the script.
    """

    def __init__(self, database_name = "tool_data"):
        """
        Initializes the SQLiteDataObject with a database name and base directory.

        Args:
            database_name (str, optional): Name of the database file without extension.
                Defaults to "tool_data".
        """
        
        self.database_name = database_name
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
    def create_sqlite_conn(self):
        """
        Creates a connection to the SQLite database.

        Returns:
            sqlite3.Connection: A connection object to the SQLite database.

        Raises:
            sqlite3.Error: If the database connection cannot be established.
        """
        db_path = f"{self.base_dir}/{self.database_name}.db"
        conn = sqlite3.connect(db_path)

        return conn
    
    def execute_sqlite_commands(self, commands):
        """
        Executes a list of SQL commands on the database.

        Args:
            commands (list): List of SQL command strings to execute.

        Raises:
            sqlite3.Error: If any SQL command fails to execute.
        """
        with self.create_sqlite_conn() as conn:
            cursor = conn.cursor()
            for command in commands:
                cursor.execute(command)

    def query_from_database(self, query):
        """
        Executes a SQL query and returns results as a pandas DataFrame.

        Args:
            query (str): SQL query string to execute.

        Returns:
            pandas.DataFrame: Query results with column names from the database.

        Raises:
            sqlite3.Error: If the query execution fails.
            AttributeError: If pandas is not available for DataFrame creation.
        """
        with self.create_sqlite_conn() as conn:
            
            cursor         = conn.cursor()
            raw_sql_output = cursor.execute(query)
            row_values     = cursor.fetchall()

        column_values = [_description[0] for _description in raw_sql_output.description]
        df = pd.DataFrame(data = row_values,
                          columns = column_values)
        
        return df
