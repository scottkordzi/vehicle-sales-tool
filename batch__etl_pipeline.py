#! A **batch** process is a process that runs every day, week, or whatever
#! An ETL pipeline is for getting our data
    #! ETL stands for Extract, Transform, Load

import pandas as pd # Python's Excel -- we'll reference it with pd
import numpy as np # Way to do lots and lots of math -- we'll reference it with np

import matplotlib.pyplot as plt

plt.style.use("ggplot")
import matplotlib.colors as mcolors

from utils.data_transfer import (pull_kaggle_data,
                                 get_create_sql_table_command,
                                 get_sql_insert_commands,
                                 import_sql_script,
                                 SQLiteDataObject)

vehicle_df = pull_kaggle_data(kaggle_path = "syedanwarafridi/vehicle-sales-data",
                              file_path_suffix = "/car_prices.csv")

ford_stock_df = pd.read_csv("data_folder/ford_stock_df.csv")

vehicle_create_table_command = get_create_sql_table_command(df = vehicle_df, 
                                                        # database_name = 'tool_data',
                                                        table_name = 'vehicle_sales_data',
                                                        primary_key_columns = ['vin', 'saledate', 'sellingprice', 'odometer'])

ford_stock_create_table_command = get_create_sql_table_command(df = ford_stock_df, 
                                                # database_name = 'tool_data',
                                                table_name = 'ford_stock_data',
                                                primary_key_columns = ['year'])

vehicle_insert_commands    = get_sql_insert_commands(df = vehicle_df.copy(deep=True),
                                                 table_name = 'vehicle_sales_data')

ford_stock_insert_commands = get_sql_insert_commands(df = ford_stock_df.copy(deep=True),
                                                 table_name = 'ford_stock_data')

sqlite_object = SQLiteDataObject(database_name = "tool_data")

sqlite_object.execute_sqlite_commands(commands = [vehicle_create_table_command])
sqlite_object.execute_sqlite_commands(commands = [ford_stock_create_table_command])

sqlite_object.execute_sqlite_commands(commands = vehicle_insert_commands)
sqlite_object.execute_sqlite_commands(commands = ford_stock_insert_commands)

dashboard_query = import_sql_script(sql_script_path = 'sql_scripts/dashboard_query.sql')

our_hard_begotten_df = sqlite_object.query_from_database(query = dashboard_query) 
