from urllib.parse import urlparse
import argparse
import logging
import re
import pandas as pd
import os
from cities_page_object import Cities
from cities_page_object import PostalCode
from retry_url import persistent_request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')

def _get_parser():
   
  parser = argparse.ArgumentParser(description='Cities scrapper by postal code and late and lone')

  parser.add_argument('--cities',
                      default= 'https://de.wikipedia.org/wiki/Liste_der_St%C3%A4dte_in_Deutschland', 
                      help='The cities args that you want to scrape', 
                      type=str
                      )
  parser.add_argument('--geo', 
                      default= 'https://nominatim.openstreetmap.org/search', 
                      help='The args where you cand find the late and lone of a city that you want to scrape', 
                      type=str
                      )
  return parser


def _get_host(url):
  parsed_url = urlparse(url)
  return f"{parsed_url.scheme}://{parsed_url.netloc}"
   

def _build_link(home_url, link):
  host = _get_host(home_url)
  if is_well_formed_link.match(link):
      return link
  elif is_root_path.match(link):
      return f'{host}{link}'
  else:
      return f'{host}/{link}'

def _get_lat_lon(url, city):
  params = {
      'q': city + ',Deutschland',  
      'format': 'json',  
      'limit': 1  
  }
  

  response = persistent_request(url, params)
  if response.status_code == 200:
    data = response.json()
    
    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon
    else:
        logger.warning('Info not found')
  else:
    return False, False

def _cities_scrapper(args):
  url_cities = args.cities
  url_geo = args.geo
  cities_object = Cities(url_cities)
  city_names = cities_object.city_name
  city_links = cities_object.city_links
  city_links_formated = [_build_link(url_cities,city_link) for city_link in city_links]
  postal_codes = []
  logger.info('tarting to scrapp postal code of each city')
  for idx, link in enumerate(city_links_formated):
    postal_code_object = PostalCode(link)
    code = postal_code_object.postal_code
    postal_codes.append(code)
    print(f'Postal code scrapped:{idx+1}')

  logger.info('Postal code of each city already scrapped!')

  city_lats = []
  city_lons = []
  for idx, city in enumerate(city_names):
    lat, lon = _get_lat_lon(url_geo, city)

    if lat and lon:
       city_lats.append(lat)
       city_lons.append(lon)
       print(f'Geolocalitation scrapped:{idx+1}')

  logger.info('Geoloaction of each city already scrapped!')

  df = pd.DataFrame({'city': city_names,
                     'postal_code': postal_codes,
                     'latitude': city_lats,
                     'longitude': city_lons})
  
  df.to_csv('../data/cities_and_postal_codes.csv', index=False)
  

      
     
if __name__ == '__main__':
  args = _get_parser().parse_args()
  if 'cities_and_postal_codes.csv' in os.listdir("../data"):
    print('Archive already created')
  else:
    _cities_scrapper(args)
  
   

