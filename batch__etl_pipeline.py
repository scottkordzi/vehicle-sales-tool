#! A **batch** process is a process that runs every day, week, or whatever
#! An ETL pipeline is for getting our data
    #! ETL stands for Extract, Transform, Load

import pandas as pd # Python's Excel -- we'll reference it with pd
import numpy as np # Way to do lots and lots of math -- we'll reference it with np

import matplotlib.pyplot as plt

plt.style.use("ggplot")
import matplotlib.colors as mcolors

from utils.data_transfer import (pull_kaggle_data,
                                 get_sql_column_datatypes)

vehicle_df = pull_kaggle_data(kaggle_path = "syedanwarafridi/vehicle-sales-data",
                              file_path_suffix = "/car_prices.csv")

# stock_df = pull_kaggle_data(kaggle_path = "syedanwarafridi/vehicle-sales-data",
#                             file_path_suffix = "/car_prices.csv")

import sqlite3

#! Define connection and cursor

conn = sqlite3.connect("tool_data.db")

cursor = conn.cursor()

vehicle_str_dtypes = get_sql_column_datatypes(df = vehicle_df.copy(deep = True))


# stock_df = get_sql_column_datatypes(df = stock_df.copy(deep = True))

#! LIST COMPREHENSION
vehicle_data_type_str = ""
for col_name, col_type in vehicle_str_dtypes.to_dict().items():
    vehicle_data_type_str = vehicle_data_type_str + f"{col_name} {col_type}, "
    
vehicle_data_type_str = vehicle_data_type_str[:-2]

#! Capitalized objects mean GLOBAL variables
PRIMARY_KEY_COLUMNS = ['vin', 'saledate', 'sellingprice', 'odometer']

primary_key_col_str = ", ".join(PRIMARY_KEY_COLUMNS)

create_vehicle_sales_table_command = f"""CREATE TABLE IF NOT EXISTS
    vehice_sales_data ({vehicle_data_type_str},
        PRIMARY KEY ({primary_key_col_str}))"""

for _, row in vehicle_df.iloc[:50].iterrows():

    iter_insert_str = f"INSERT INTO vehice_sales_data VALUES {tuple(row.values)}"
    iter_insert_str = iter_insert_str.replace(" nan,", " NULL,")
    cursor.execute(iter_insert_str)

cursor.execute(create_vehicle_sales_table_command)

vehicle_sales_query = """
SELECT vin
     , saledate
     , sellingprice
     , make
     , model
FROM vehice_sales_data;
"""

cursor.execute(vehicle_sales_query).fetchall()