This app is in charge of doing web scraping to obtain all the cities, their zip codes and geographic coordinates (latitude and longitude) and return given a city or a zip code, return the zip codes in a given radius. The app was made in a modular way so that it can be used if the web scraping link varies.

###IMPORTANT I push to the repository the csv result of my scrapping but if you want to test the entire app just deleted and the app will start from the beginning


##The app have the next structure:
.
├── data
│   ├── cities_and_postal_codes.csv
│   └── cities_postal_code_clean.csv
├── extract
│   ├── cities_page_object.py
│   ├── common.py
│   ├── config.yaml
│   ├── main.py
│   └── retry_url.py
├── load
│   └── main.py
├── pipeline.py
├── README.md
└── transform
    └── main.py

#For run the app you just have to write in the terminal: python pipeline.py

#You can modify the css selector for scraping if you modify the config.yaml file

#Thanks!

