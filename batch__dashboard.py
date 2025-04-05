import pandas as pd
import sqlite3

#! TO-DO
    #! Put SQL script in separate SQL file
    #! Create functions for different SQLite stuff

#! "WHERE" and "HAVING" are both data filters, but HAVING allows for aggregations,
#! such as AVG(), whereas WHERE does *NOT* 

conn = sqlite3.connect("tool_data.db")

cursor = conn.cursor()
'hey' 
"hey"
"""This is a DOC STRING"""


vehicle_sales_query = """
SELECT vsd.year
     -- , vsd.vin
     -- , vsd.saledate
     , AVG(vsd.sellingprice) AS avg_selling_price
     -- , vsd.make
     -- , vsd.model
FROM vehicle_sales_data AS vsd
WHERE (vsd.year > 2000)
GROUP BY vsd.year
-- HAVING AVG(vsd.sellingprice) < 20000
;
"""

#! Runs SQL command
raw_sql_output = cursor.execute(vehicle_sales_query)

row_values = raw_sql_output.fetchall()
#! List comprehension automatically CREATES A LIST
column_values = [_description[0] for _description in raw_sql_output.description]

vehicle_df = pd.DataFrame(data = row_values,
                          columns = column_values)

