import os
import requests
import pandas as pd
from math import log
from bs4 import BeautifulSoup
import pypopulation as pp
from serpapi import GoogleSearch
import country_converter as coco
from geopy import distance as dist
from geopy.geocoders import Nominatim
from countryinfo import CountryInfo as ci

# Initialize Nominatim API
geolocator = Nominatim(user_agent="coincidencesInLocation")

def print_full_rows(x):
    """
    Print full rows of a dataset
    """
    pd.set_option('display.max_rows', None)
    print(x)
    pd.reset_option('display.max_rows')


def print_full_cols(x):
    """
    Print full columns of a dataset
    """
    pd.set_option('display.max_columns', None)
    print(x)
    pd.reset_option('display.max_columns')


def compute_death_country(lat, long):
    """
    Computes the country of a person according to 
    the latitude (lat) and logitude (long) provided
    """
    location = geolocator.reverse(str(lat) + "," + str(long), language='en')
    address = location.raw['address']

    return address.get('country')


def compute_description(lat_p1, lat_p2, long_p1, long_p2, district_size=20):
    """
    Computes the description complexity considering 
    the distance between places.
    The `const` param accounts for the size of the villages
    """
    d_p1 = (lat_p1, long_p1)
    d_p2 = (lat_p2, long_p2)

    distance = dist.distance(d_p1, d_p2).km

    return int(log(1 + distance/district_size, 2))


def compute_generation(country, district_size=20):
    """
    Computes the generation complexity of a country
    """
    country_iso2 = coco.convert(names=[country], to='ISO2')
    pop = pp.get_population(country_iso2)
    area = ci(country).area() / district_size**2

    return int(log(pop, 2) + log(area, 2))


def get_city_name(lat, long):
    """
    Returns the name of the city from latitude (lat) and
    longitude (long) provided
    """
    location = geolocator.reverse((lat, long))
    
    address = location.raw['address']
    city = address.get('city')

    # account for different features to avoid none
    if city is None:
        city = address.get('town')
        
    if city is None:
        city = address.get('village')
        
    if city is None:
        city = address.get('country')
        
    if city is None:
        city = address.get('state')

    return city


def define_constants(person, df):
    """
    Returns the main informations about the person
    """
    # latitude
    lat_birth = df['birth_latitude'].values[person]
    lat_death = df['death_latitude'].values[person]

    # longitude
    lon_birth = df['birth_longitude'].values[person]
    lon_death = df['death_longitude'].values[person]

    # countries
    country_birth = df['country'].values[person]
    country_death = compute_death_country(lat_death, lon_death)

    # name
    name = df['name'].values[person]

    # main area
    area = df['main_area'].values[person]

    return name, lat_birth, lat_death, lon_birth, lon_death, country_birth, country_death, area

def get_results_web(query):
    """
    Return number of hints on Google for a certain query
    """
    params = {
        "engine": "google",
        "q": query,
        #"api_key": os.getenv("myApiKeySerp")
        "api_key": "e5028cd3407eed65fcede5f70821cdf8b1dac2310fbab567e092ab2961d985ec"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    print(results)

    return results["search_information"]['total_results']

def get_results_web2(query):
    r = requests.get('http://www.google.com/search',
                     params={'q': query,
                             "tbs": "li:1"})
    r.raise_for_status()

    soup = BeautifulSoup(r.text)