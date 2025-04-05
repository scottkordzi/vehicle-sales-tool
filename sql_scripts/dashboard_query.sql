SELECT * 
FROM vehicle_sales_data -- AS vsd
INNER JOIN ford_stock_data -- AS fsd
USING(year)
WHERE year >= 2000;