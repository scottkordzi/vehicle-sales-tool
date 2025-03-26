import pandas as pd # Python's Excel -- we'll reference it with pd
import numpy as np # Way to do lots and lots of math -- we'll reference it with np

import matplotlib.pyplot as plt

plt.style.use("ggplot")
import matplotlib.colors as mcolors

from utils.data_transfer import pull_kaggle_data

vehicle_df = pull_kaggle_data(kaggle_path = "syedanwarafridi/vehicle-sales-data",
                              file_path_suffix = "/car_prices.csv")


number_of_x_var_in_each_bin = 1
variable_min = min(vehicle_df['year'])
variable_max = max(vehicle_df['year'])

bin_starts = list(range(variable_min, 
                        variable_max + 1, 
                        number_of_x_var_in_each_bin))

fig, ax = plt.subplots(ncols=1, nrows=1)

ax.hist(vehicle_df['year'],
        alpha = 0.8,
        bins = bin_starts)
ax.set_xlabel("year")
ax.set_ylabel("Count")
ax.set_title("Vehicle Sales by Year")
ax.axvline(2008, 
            color = 'black',
            linestyle = '-.',
            label = 'Financial Crash of 2008',
            alpha = 0.8)
ax.legend()
plt.show()



number_of_x_var_in_each_bin = 1
variable_min = min(vehicle_df['condition'])
variable_max = max(vehicle_df['condition'])

bin_starts = list(range(int(variable_min), 
                        int(variable_max) + 1, 
                        number_of_x_var_in_each_bin))

fig, ax = plt.subplots(ncols=1, nrows=1)

ax.hist(vehicle_df['condition'],
        alpha = 0.8,
        bins = bin_starts)
ax.set_xlabel("Condition")
ax.set_ylabel("Count")
ax.set_title("Vehicle Sales by Condition")
ax.legend()
plt.show()


#! CAPITALIZED object means it is a GLOBAL VARIABLE
COLOR_DICT = mcolors.CSS4_COLORS
#! LIST COMPREHENSION with an IF STATEMENT
    #! List comprehension are kinda backwards
    #! output comes before the for loop
DARK_COLORS = [color for color in COLOR_DICT.keys()
                     if 'dark' in color]
#! Want function to take _list as an argument and print out each element

def print_elements(_list):
        
    for color in DARK_COLORS:
        print(color)

print_elements(_list = ['all', 'the', 'things', 0])


def print_elements(_list):
        
    for element in _list:
        print(element)

float(vehicle_df['sellingprice'].mean())

list(vehicle_df.groupby('year'))[0][0]

vehicle_df_for_1988 = list(vehicle_df.groupby('year'))[6][1]

float(vehicle_df_for_1988['sellingprice'].mean())
count_of_cars_sold_by_year = vehicle_df.groupby('year')['sellingprice'].count()

count_threshold_criteria = count_of_cars_sold_by_year > 50

avg_selling_price_by_year = vehicle_df.groupby('year')['sellingprice'].mean()

avg_selling_price_by_year[count_threshold_criteria].plot()


print_elements(_list = ['all', 'the', 'things', 0])
print_elements(_list = DARK_COLORS)
#! Defining a custom function
    #! We create functions bc we dont want to write the same lines of code
    #! more than once 
    #! Good practice is to start with a VERB like 'get_'
def get_histogram(df, 
                  col_of_interest = 'year', #! 'year' is the DEFAULT ARGUMENT of col_of_interest
                  hist_title = 'Vehicle Sales by year',
                  number_of_x_var_in_each_bin = 1,
                  vertical_line_dict = {'Financial Crash of 2008' : 2008,
                                        'Internet Stock Market Crash of 2001' : 2001,
                                        'Birth of Scott': 1998}
                  ):

    #! Functions contain LOCAL variables, everything outside of 
    #! them is global
    variable_min = min(df[col_of_interest])
    variable_max = max(df[col_of_interest])

    bin_starts = list(range(int(variable_min), 
                            int(variable_max) + 1, 
                            number_of_x_var_in_each_bin))

    fig, ax = plt.subplots(ncols=1, nrows=1)

    ax.hist(df[col_of_interest],
            alpha = 0.8,
            bins = bin_starts)
    ax.set_xlabel(col_of_interest)
    ax.set_ylabel("Count")
    ax.set_title(hist_title)

    if len(vertical_line_dict) > 0:
        i = 0
        for label, value in vertical_line_dict.items():
            ax.axvline(value, 
                        color = DARK_COLORS[i],
                        linestyle = '-.',
                        label = label,
                        alpha = 0.8)
            i = i + 1
    
    ax.legend()

    #! This is the object(s) we are RETURNING 
    return fig


yearly_histogram = get_histogram(df = vehicle_df, 
                                col_of_interest = 'year',
                                hist_title = 'Vehicle Sales by year',
                                number_of_x_var_in_each_bin = 1,
                                vertical_line_dict = {'Financial Crash of 2008' : 2008,
                                                        'Internet Stock Market Crash of 2001' : 2001,
                                                        'Birth of Scott': 1998}
                                )

condition_histogram = get_histogram(df = vehicle_df, 
                                col_of_interest = 'condition',
                                hist_title = 'Vehicle Sales by Condition',
                                number_of_x_var_in_each_bin = 1,
                                vertical_line_dict = {}
                                )

vertical_line_dict = {'Financial Crash of 2008' : 2008,
                    'Internet Stock Market Crash of 2001' : 2001,
                    'Birth of Scott': 1998}

def print_key_value_pairs(_dict):

    for key, value in _dict.items():
        # key, value = list(_dict.items())[0]
        print(key, value)

print_key_value_pairs(_dict = vertical_line_dict)

vehicle_df['year'].hist(bins = bins)
plt.xlabel("year")
plt.ylabel("Count")

vehicle_df['condition'].hist()

#! A line plot
vehicle_df.sort_values("odometer").plot('odometer')

#!######

ages = [30, 18, 19, 21, 25, 26, 26, 30, 32, 38, 45, 55]

def personal_info(age, ages):

    ages = sorted(ages)

    age_found = False
    for i, iter_age in enumerate(ages):

        if iter_age == age:
            print(f"My age is {age} and I fit in as an element that is first indexed at {i}")
            age_found = True
            break

    if age_found == False:
        print("Well shit, that age isn't a part of our list. Guess we should go die now.")

personal_info(int(input("What is your age?")), ages = ages)
