import requests
import urllib3
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import numpy as np
import tkinter as tk ##placeholder for later usage##
import streamlit as st
import base64
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import streamlit.components.v1 as components
from pandas.io.json import json_normalize
from datetime import date
import json

##URL for webscraping National U.S COVID Data
html_text = requests.get('https://www.worldometers.info/coronavirus/country/us/')
soup = BeautifulSoup(html_text, 'lxml')
webscrapenum = soup.findall('li', class_ = 'maincounter-number')

today = date.today()


#Streamlit Main Webpage Header and Info
st.title('COVID-19 Utility Web Application')
st.markdown("""
* **Python libraries:** urllib3, numpy, tkinter, streamlit, beautifulsoup4, base64, seaborn, pandas, matplotlib
* **Data source (COVID Data API):** [COVID-Act-Now.com](https://apidocs.covidactnow.org/)""")
st.write("""
This webpage uses COVID Data API to gather accurate data and present it in one place.

**This is an early version of the program, please do not take COVID data presented here as an accurate reflection.**
***
""")


sidebar_selection = st.sidebar.radio(
    'Select data:',
    ['Select Counties', 'U.S'],
)

st.header('Enter corresponding information into your console/terminal')

st.subheader('COVID Data for State and County:')
selected_state = st.sidebar.selectbox('State', dict())
selected_county = st.sidebar.selectbox('County', dict())

st.dataframe(df_selected_sector)
#df = load_data()
sorted_sector_unique = sorted( df['Total U.S COVID Cases']).unique() )
sorted_sector_unique = sorted( df['Total U.S COVID Deaths']).unique() )
sorted_sector_unique = sorted( df['Total U.S COVID Recovered Cases']).unique() )
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique)



##State COVID Data **needs fixing**
state_url = "https://api.covidactnow.org/v2/states.json?apiKey=c4edd54144b943c68a637a1b64194c0c"
response = requests.get(state_url)
data = response.json()

##County-level COVID Data **needs fixing**
county_url = "https://api.covidactnow.org/v2/counties.json?apiKey=c4edd54144b943c68a637a1b64194c0c"
response = requests.get(county_url)
data = response.json()
states = [x["state"] for x in data]
cases = [x["actuals"]["cases"] for x in data]
##deaths = [x["actuals"]["deaths"] for x in data]

counties = [x["county"] for x in data]
cases = [x["actuals"]["cases"] for x in data]
print(cases)

dictionary_1 = dict(zip(states, cases))
dictionary_2 = dict(zip(counties, cases))
##dictionary = dict(zip(states, deaths))



#US State Data and Abbreviations
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
## US State County Data


## U.S State Input
inp = False
state_key = ""

while (inp == False):
    try:
        state = input("Please enter a state: ")
        state = state.lower()
        state = state.title()
        state_key = us_state_to_abbrev[state]
        print(state_key)
        inp = True
    except:
        print("Try again")

## US State County Input
inp = False
county_key = ""

while (inp == False):
    try:
        county = input("Please enter a county: ")
        county = county.lower()
        county = county.title()
        county_key = us_state_county[county]["name"]
        print(county_key)
        inp = True
    except:
        print("Try again")

#mainline console print
print("There are " + str(dictionary_1[state_key]) + " total confirmed COVID-19 cases in " + state)
print("There are " + str(dictionary_2[county_key]) + " total confirmed COVID-19 cases in " + county)

#streamlit webpage print
st.write("There are " + str(dictionary_1[state_key]) + " total confirmed COVID-19 cases in " + state)
st.write("There are " + str(dictionary_2[county_key]) + " total confirmed COVID-19 cases in " + county)
##print("There are " + str(dictionary[state_key]) + " total deaths in " + state)