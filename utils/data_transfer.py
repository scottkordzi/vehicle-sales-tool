import pandas as pd
import kagglehub


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
