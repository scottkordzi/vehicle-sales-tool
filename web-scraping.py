from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(executable_path = '/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service = service)
url = driver.get("https://www.carpro.com/")

search = driver.find_element(By.CLASS_NAME, "site-header__search-trigger")
search.click()
search.send_keys("Full-Year Auto Sales Report" + Keys.ENTER)
links = driver.find_element(By.PARTIAL_LINK_TEXT, "Full-Year Auto Sales Report")
links.click()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table.table.table-bordered.table-striped"))
)

soup = BeautifulSoup(driver.page_source, 'lxml')

table = soup.find('table', class_='table table-bordered table-striped')

headers = table.find_all('td')

titles = []
for i in headers[:3]:
    title = i.text.replace('\xa0', '').replace('vs', '').replace('2024', 'sales_numbers').replace('2023', 'percent_change_2023').strip()
    titles.append(title)

titles.append('year')

auto_sales_df = pd.DataFrame(columns = titles)

column_data = table.find_all('tr')

for row in column_data[1:]:
    row_data = row.find_all('td')
    individual_row_data = [data.text.strip() for data in row_data]
    individual_row_data.append('2024')

    length = len(auto_sales_df)
    auto_sales_df.loc[length] = individual_row_data

auto_sales_df['sales_numbers'] = pd.to_numeric(
    auto_sales_df['sales_numbers'].str.replace(',', '').str.replace(' ', ''),
    errors='coerce')

auto_sales_df['percent_change_2023'] = pd.to_numeric(
    auto_sales_df['percent_change_2023'].str.replace('%', '').str.replace(' ', ''),
    errors='coerce')

auto_sales_df['sales_numbers'] = auto_sales_df['sales_numbers'].fillna(0)
auto_sales_df['percent_change_2023'] = auto_sales_df['percent_change_2023'].fillna(0)

auto_sales_df.to_csv('data_folder/2024_us_auto_sales.csv', index=False)
driver.quit()