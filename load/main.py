import pandas as pd
import argparse
import numpy as np
import logging
import warnings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _get_parser():
    parser = argparse.ArgumentParser(description='Search the near city')    
    parser.add_argument('--cities',
                        default= '../data/cities_postal_code_clean.csv', 
                        help='The path of the csv with the cities and their postal codes', 
                        type=str
                        )   
    return parser

def _search(csv_path):
    print('\nHow do you want search by city name or by postal code')
    option = int(input('Select 1 for city name and 2 for postal code: '))
    if option == 1:
        response, radius = _input(option)
        print(radius)
        result = _search_by_city(csv_path, response, radius)
        print(result)
    elif option == 2:
        response, radius = _input(option)
        result = _search_by_postal_code(csv_path, response, radius)
        print(result)
    else:
        logger.warning('Option incorrect please select a the correct options: 1 for city name and 2 for postal code')



def _search_by_city(csv_path, key, radius):
    df = pd.read_csv(csv_path)
    if radius <= 0:
        logger.warning('Incorrect radius, entry a positive radius')
        return 'Radius error'
    
    if df['city'].isin([key]).any():
        lat = df[df['city'] == key]['latitude']
        lon = df[df['city'] == key]['longitude']

        length = df.apply(lambda row: _calculate_near(lon, lat, row['longitude'], row['latitude']), axis=1)

        df['length'] = length

        return df[df['length'] <= radius]['postal_code'].values
          
    else:
        logger.warning('Incorrect city please select a correct city name. For more information about city names please go to: https://de.wikipedia.org/wiki/Liste_der_St%C3%A4dte_in_Deutschland ')
        return 'City error'
        


def _search_by_postal_code(csv_path, key, radius):
    df = pd.read_csv(csv_path) 
    if radius <= 0:
        logger.warning('Incorrect radius, entry a positive radius')
        return 'Radius error'
    
    value = df['postal_code'].apply(lambda x: key in [cp.strip() for cp in x.split(',')]).isin([True]).any()
    if value:

        index = df.index[df['postal_code'].apply(lambda x: key in [cp.strip() for cp in x.split(',')])].tolist()

        lat = df.loc[index, 'latitude'].values[0]
        lon = df.loc[index, 'longitude'].values[0]
        
        length = df.apply(lambda row: _calculate_near(lon, lat, row['longitude'], row['latitude']), axis=1)

        df['length'] = length

        return df[df['length'] <= radius]['postal_code'].values
    else:
        logger.warning('Incorrect postal code please select a correct postal code. For more information about city names please go to: https://de.wikipedia.org/wiki/Liste_der_St%C3%A4dte_in_Deutschland ')
        return 'Postal Code Error'


def _calculate_near(key_lat, key_lon, df_lat, df_lon):
    warnings.filterwarnings("ignore")
    lon1, lat1, lon2, lat2 = map(np.radians, [key_lon, key_lat, df_lon, df_lat])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = np.sin(dlat/2)**2 + np.cos(key_lat) * np.cos(df_lat) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    r = 6371 
    
    return r*c

def _input(option):
    if option == 1:
        string = input('Enter the city name: ')
    elif option == 2:
        string = input('Enter the postal code: ')
    
    radius = int(input('Enter the radius(km): '))

    return string, radius

if __name__ == '__main__':
    args = _get_parser().parse_args()
    _search(args.cities)
    