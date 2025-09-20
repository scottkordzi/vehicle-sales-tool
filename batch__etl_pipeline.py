import pandas as pd 
import numpy as np 

from utils.data_transfer import (pull_kaggle_data,
                                 get_create_sql_table_command,
                                 get_sql_insert_commands,
                                 SQLiteDataObject)

vehicle_df    = pull_kaggle_data(kaggle_path = "syedanwarafridi/vehicle-sales-data",
                                 file_path_suffix = "/car_prices.csv")

ford_stock_df = pd.read_csv("data_folder/ford_stock_df.csv")

auto_sales_df = pd.read_csv("data_folder/2024_us_auto_sales.csv")

vehicle_create_table_command    = get_create_sql_table_command(df = vehicle_df, 
                                                               table_name = 'vehicle_sales_data',
                                                               primary_key_columns = ['vin', 'saledate', 'sellingprice', 'odometer'])

ford_stock_create_table_command = get_create_sql_table_command(df = ford_stock_df, 
                                                                table_name = 'ford_stock_data',
                                                                primary_key_columns = ['year'])

auto_sales_create_table_command = get_create_sql_table_command(df = auto_sales_df, 
                                                               table_name = 'auto_sales_comparison',
                                                               primary_key_columns = ['year', 'Manufacturer'])

vehicle_insert_commands    = get_sql_insert_commands(df = vehicle_df.copy(deep=True),
                                                     table_name = 'vehicle_sales_data')

ford_stock_insert_commands = get_sql_insert_commands(df = ford_stock_df.copy(deep=True),
                                                     table_name = 'ford_stock_data')

auto_sales_insert_commands = get_sql_insert_commands(df = auto_sales_df.copy(deep=True),
                                                     table_name = 'auto_sales_comparison')

sqlite_object = SQLiteDataObject(database_name = "tool_data")


sqlite_object.execute_sqlite_commands(commands = [vehicle_create_table_command])
sqlite_object.execute_sqlite_commands(commands = [ford_stock_create_table_command])
sqlite_object.execute_sqlite_commands(commands = [auto_sales_create_table_command])

sqlite_object.execute_sqlite_commands(commands = vehicle_insert_commands)
sqlite_object.execute_sqlite_commands(commands = ford_stock_insert_commands)
sqlite_object.execute_sqlite_commands(commands = auto_sales_insert_commands)