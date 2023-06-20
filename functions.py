import os
import csv
import pandas as pd
from math import log, ceil
import pypopulation as pp
import country_converter as coco
from geopy import distance as dist
from geopy.geocoders import Nominatim
from countryinfo import CountryInfo as ci

# Initialize Nominatim API
geolocator = Nominatim(user_agent="coincidencesInLocation", timeout=30)

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
    #print(lat, long)
    location = geolocator.reverse(str(lat) + "," + str(long), language='en')
    
    if location is not None:
        address = location.raw['address']
        return address.get('country')
    else:
        return 'non found'


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

    # hits
    hits = df['popularity'].values[person]

    return name, lat_birth, lat_death, lon_birth, lon_death, country_birth, country_death, area, hits


def write_file(data, version):
    """
    Write the results in a 'csv' file
    """
    file_name = version + '.csv'
    file_path = os.path.join("../tests/", file_name)

    # open a file with possibility to rewrite
    with open(file_path, "a", newline="", encoding="utf-8") as file:
        w = csv.writer(file)
        w.writerows(data)


def simplicity_person(category, log_hints, desc_music, desc_actor):
    """
    Calculates the simplicity of a person based on very popular
    people in the category
    """
    if category == 'music':
        desc_complexity = ceil(desc_music / (1+log_hints))    # avoid division by 0 in denominator
    elif category == 'actor':
        desc_complexity = ceil(desc_actor / (1+log_hints))
    
    return desc_complexity