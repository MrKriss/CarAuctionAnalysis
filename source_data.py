"""Functions to fetch, parse and encode updated data from centralcarauctions.com.

Functions
---------
fetch_all_html_entries:
    Fetching most recent webpage and extracting the relevant tags for car details
parse_html_entries:
    Extract data from the list of HTML tags into a pandas data frame.
preprocess:
    Data pre-processing/filtering/munging/data type convertion.
encode:
    Feature Encoding of categorical variables.
load_data_from_disk:
    Load all data structures from disk instead of redownloading them. Also performs 
    necessary type conversions.

Directly executing this script runs the first four functions in sequence. 

Full list of cars and prices sourced from:
http://www.centralcarauctions.com/trade/vehicles/price-guide

"""

from collections import defaultdict
import requests
import pickle

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def fetch_all_html_entries():
    """Fetch up to date data for all auctions from HTML page.

    Returns
    -------
    all_entries : list of BeautifulSoup objects
        Lists the html tags that hold the car auction data, one observation per
        element.
    """
    # Template string to format with URL parameters for page and pageSize
    target_url = "http://www.centralcarauctions.com/trade/vehicles/price-guide?page={}&pageSize={}"

    # Read entries in batches of 1000, iterating untill no more cars are found 
    page_count = 1
    still_cars = True
    all_entries = []
    while still_cars:

        result = requests.get(target_url.format(page_count, 1000))

        assert result.status_code == 200, \
            "Connection Error: status code = {}".format(result.status_code)

        soup = BeautifulSoup(result.content)
        entries = soup.find_all('li', class_="p-g-item") 
        if entries:
            all_entries.extend(entries)
            page_count += 1
        else:
            still_cars = False

    print('Total of {} cars returned'.format(len(all_entries)))

    return all_entries


def parse_html_entries(entries_list, output_file=None):
    """Parse a list of HTML tags to rows of a data frame.

    Parameters
    ----------
    entries_list : list
        List of BeautifulSoup Objects.
    output_file : str
        File name to write output to if given.    

    Returns
    -------
    df_raw : DataFrame
        Raw data passed from HTML page.
    """
    data_dict = defaultdict(list) 

    for ent in entries_list:
        items = ent.find_all('span')
        data_dict['make'].append(str(items[0].string))
        
        text = items[1].string.split(' ')
        data_dict['model'].append(text[0])
        data_dict['trim'].append(' '.join(text[1:]))
        
        data_dict['class'].append(str(items[2].string))
        data_dict['year'].append(str(items[4].string))
        data_dict['MOT'].append(str(items[6].string))
        data_dict['mileage'].append(str(items[8].string))
        data_dict['price'].append(str(items[9].string))

    data_headers = ['make', 'model', 'trim', 'class', 'year', 'mileage', 'MOT', 'price']
    df_raw = pd.DataFrame(data_dict, columns=data_headers)
    
    if output_file:
        df_raw.to_csv(output_file, index=False)

    return df_raw


def preprocess(df_raw, output_file=None):
    """"Return a copy of raw dataframe after preprocessing.

    Preprocessing includes handling missing values, outliers and type convertions.

    Parameters
    ----------
    df_raw : DataFrame
        The raw data frame pased from HTML.
    output_file : str
        File name to write output to if given.   

    Returns
    -------
    df_pro : DataFrame
        The preprocessed data frame 

    """
    # Work with a copy of the original data
    df_pro = df_raw.copy()

    # Convert MOT and Year to date time 
    df_pro.MOT = df_raw.MOT
    df_pro.MOT = pd.to_datetime(df_raw.MOT, format='%b %Y', coerce=True)
    df_pro.year = df_raw.year
    df_pro.year = df_raw.year.str.replace(pat=' \(.+\)', repl='')
    df_pro.year = pd.to_datetime(df_pro.year, format='%b %Y')

    # Strip commas and missing values
    df_pro.mileage = df_pro.mileage.str.replace(',', '')
    df_pro.mileage = df_pro.mileage.str.replace('not showing', 'NAN')
    df_pro.mileage = df_pro.mileage.str.replace('not shown', 'NAN')
    df_pro.mileage = df_pro.mileage.str.replace('Not Showing', 'NAN')
    df_pro.mileage = df_pro.mileage.str.replace('.', 'NAN')
    
    # Convert km to miles
    km_idx = df_pro.mileage.str.contains('km')
    for idx in km_idx.nonzero()[0]:
        df_pro.loc[idx, 'mileage'] = 5 * int(df_pro.loc[idx, 'mileage'].split(' ')[0]) / 8. 
    df_pro.mileage = df_pro.mileage.astype(float)
    
    # Convert price to string, remove commas and pound sign, then store as float. 
    df_pro.price = df_pro.price.str.replace(',', '')
    df_pro.price = df_pro.price.str.replace(u'\xa3', '')
    df_pro.price = df_pro.price.astype(float)

    if output_file:
        df_pro.to_csv(output_file, index=False)

    return df_pro


def encode(df_pro, output_file=None):
    """Return a copy of preprocessed data frame after encoding.

    Encoding includes mapping unique categorical values to integers. The mapping
    is stored in the array objects [MOT, year, model, make, class]_decoder which 
    are the sorted unique values in each column. These are returned collectively 
    in a dictionary

    Therefore the original can be retrieved with:
        decoders[column_name][integer_encoding]

    Parameters
    ----------
    df_pro : DataFrame
        The preprocessed data frame.
    output_file : str
        File name to write output to if given.   

    Returns
    -------
    df_enc : DataFrame
        The encoded DataFrame
    decoders : dict
        Keys are the column names encoded, and the values are the arrays that hold
        the sorted unique values for that column. There index corresponds to the 
        integer used to encode them. 

    """
    # Work with a copy of the original data
    df_enc = df_pro.copy()
    
    # Ecode Dates as ordinals in extra column as date time values still useful for plots
    MOT_decoder = np.unique(df_enc["MOT"])
    df_enc['MOT_ord'] = np.unique(df_enc["MOT"], return_inverse=True)[1]
    
    year_decoder = np.unique(df_enc["year"])
    df_enc['year_ord'] = np.unique(df_enc["year"], return_inverse=True)[1]
    
    model_decoder = np.unique(df_enc["model"])
    df_enc["model"] = np.unique(df_enc["model"], return_inverse=True)[1]
    
    make_decoder = np.unique(df_enc["make"])
    df_enc["make"] = np.unique(df_enc["make"], return_inverse=True)[1]
    
    class_decoder = np.unique(df_enc['class'])
    df_enc['class'] = np.unique(df_enc['class'], return_inverse=True)[1]

    # Encode NaN as a very high number
    df_enc.loc[df_enc.mileage.isnull(), 'mileage'] = 9999999

    decoder = {'MOT': MOT_decoder, 
               'year': year_decoder, 
               'model': model_decoder, 
               'make': make_decoder, 
               'class': class_decoder}

    with open('decoder.pkl', 'wb') as f:
        pickle.dump(decoder, f)

    if output_file:
        df_enc.to_csv(output_file, index=False)

    return df_enc, decoder


def load_data_from_disk():
    """ Load in data frames and decoder from disk. 

    Data stored as csv files and pickle files. Datatime conversions also done 
    for MOT and year columns.

    Returns
    -------
    df_raw:  Raw DataFrame
    df_pro:  Processed DataFrame 
    df_enc:  Encoded DataFrame
    decoder: Dictionary of decoders for encoded columns
    """

    df_raw = pd.read_csv('cca_data_raw.csv')
    df_pro = pd.read_csv('cca_data_pro.csv')
    df_enc = pd.read_csv('cca_data_enc.csv')
    decoder = pickle.load(open('decoder.pkl', 'rb'))

    # Convert date strings to numpy datetime objects
    # For processed df
    if df_pro["MOT"].dtype == 'O': 
        df_pro["MOT"] = pd.to_datetime(df_pro["MOT"])  
    if df_pro["year"].dtype == 'O': 
        df_pro["year"] = pd.to_datetime(df_pro["year"])  
    # For encoded df
    if df_enc["MOT"].dtype == 'O': 
        df_enc["MOT"] = pd.to_datetime(df_enc["MOT"])  
    if df_enc["year"].dtype == 'O': 
        df_enc["year"] = pd.to_datetime(df_enc["year"])  

    MOT_decoder = np.unique(df_pro["MOT"])    
    year_decoder = np.unique(df_pro["year"])
    model_decoder = np.unique(df_pro["model"])
    make_decoder = np.unique(df_pro["make"])
    class_decoder = np.unique(df_pro['class'])
    
    decoder = {'MOT': MOT_decoder, 
               'year': year_decoder, 
               'model': model_decoder, 
               'make': make_decoder, 
               'class': class_decoder}

    return df_raw, df_pro, df_enc, decoder

if __name__ == '__main__':
    
    df_raw = parse_html_entries(fetch_all_html_entries(), output_file='cca_data_raw.csv')
    df_pro = preprocess(df_raw, output_file='cca_data_pro.csv')
    df_enc, decoder = encode(df_pro, output_file='cca_data_enc.csv')
