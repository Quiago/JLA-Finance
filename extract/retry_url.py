import requests
import time

def persistent_request(url, params=None):
    """sumary_line
    A function to keep trying to connect to the url if we have internet problems the scrapper does not stop by this
    Keyword arguments:
    argument -- url string --params a dcitionary with params that the url required to send
    Return: response of the request
    """
    
    while True:
        try:
            response = requests.get(url, params)
            if response.status_code == 200:
                print("Successful connection!")
                return response
            else:
                print('Something wrong with your url')
        except Exception as e:
            print(f"Request error: {e}. Retrying...")
            time.sleep(1)
            