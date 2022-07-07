# This is a very simple python code where have a method data_cleaner.
# Inside it, first we are reading the csv file.
# After reading, we have three different functions preforming the data cleaning process.

def data_cleaner():

    import pandas as pd
    import re

    df = pd.read_csv("~/store_files_airflow/raw_store_transactions.csv")


    # The 1st is clean_store_location.
    # This function will remove any special symbols from the store_location column.

    def clean_store_location(st_loc):
        return re.sub(r'[^\w\s]', '', st_loc).strip()


    # The 2nd function clean_product_id, will clean the product id column.
    # This method will remove any other characters other than integer, hence returning only integer value.

    def clean_product_id(pd_id):
        matches = re.findall(r'\d+', pd_id)
        if matches:
            return matches[0]
        return pd_id

    # Then we have a ‘remove_dollar’ function which will remove the dollar sign from all the price columns.
   

    def remove_dollar(amount):
        return float(amount.replace('$', ''))

     # The next two lines are giving call to clean_store_location and clean_product_id functions.
     

    df['STORE_LOCATION'] = df['STORE_LOCATION'].map(lambda x: clean_store_location(x))
    df['PRODUCT_ID'] = df['PRODUCT_ID'].map(lambda x: clean_product_id(x))


    # For remove_dollar function, since we have four columns having dollar sign, so we are calling it inside a ‘for’ loop each loop for one column.
    for to_clean in ['MRP', 'CP', 'DISCOUNT', 'SP']:
        df[to_clean] = df[to_clean].map(lambda x: remove_dollar(x))


    # At last, after all the functions ran, we are saving the clean data in a new clean_store_transactions file which would be placed in the same directory where raw file was placed.
    # That’s it for this function.

    df.to_csv('~/store_files_airflow/clean_store_transactions.csv', index=False)


