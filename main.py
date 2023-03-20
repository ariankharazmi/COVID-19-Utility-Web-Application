import time

import matplotlib
import requests
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from altair.examples.pyramid import df
import numpy as np
import streamlit as st
import base64
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter, WeekdayLocator
from matplotlib.ticker import NullFormatter
import matplotlib as mpl
import matplotlib.style as style
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import RendererAgg
import matplotlib.dates as dates
import altair as alt
import streamlit.components.v1 as components
from pandas.io.json import json_normalize
from datetime import date
import json

from streamlit.elements.selectbox import SelectboxMixin
from urllib3.util import url
mpl.use("agg")

from statedata import us_state_to_abbrev
from statedata import us_state_list
from statedata import us_state_fip
from countydata import us_state_county
from countrydata import country_list

style.use('fivethirtyeight')
plt.rcParams['lines.linewidth'] = 1
dpi = 1000
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = plt.rcParams['font.size']
plt.rcParams['axes.titlesize'] = plt.rcParams['font.size']
plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']
plt.rcParams['figure.figsize'] = 6, 6

apiKey = 'c4edd54144b943c68a637a1b64194c0c'

_ENABLE_PROFILING = False

if _ENABLE_PROFILING:
    import cProfile, pstats, io
    from pstats import SortKey
    pr = cProfile.Profile()
    pr.enable()



#Streamlit Main Webpage Header and Info
st.title('COVID-19 Utility Web Application')
ts = int(time.time())
today = date.today()
print(today)

st.write("""You are visiting on:    """ + str(today))
st.markdown("""
* **Data sources: COVID Data API(s):** [Centers for Disease Control (CDC)](https://apidocs.covidactnow.org/), [Worldometers](https://github.com/CSSEGISandData/COVID-19), [New York Times](https://github.com/nytimes/covid-19-data)""")


st.write("""
This webpage uses COVID-19 Data from different API sources to gather accurate data and present it in one place.

**This is an early version of the program, please do not take COVID-19 data presented here as an accurate reflection.**
***
""")


sidebar_selection = st.sidebar.radio(
    'Select location data to display:',
    ['Show All', 'Show Country', 'Show U.S State', 'Show U.S County'],
)
sidebar_selection = st.sidebar.radio(
    'Select which data source to display:',
    ['Show All Sources', 'Show CDC Data ', 'Show Worldometers Data', 'Show New York Times Data'],
)



st.header('Please enter corresponding information into the boxes below.')

st.subheader('Display COVID-19 data based on user inputs')
selected_country = st.sidebar.selectbox('Country', dict())
selected_state = st.sidebar.selectbox('State', dict())
selected_county = st.sidebar.selectbox('County', dict())


dictionary_1 = country_list
dictionary_2 = us_state_fip, us_state_list, us_state_to_abbrev
dictionary_3 = us_state_county

# Streamlit Webpage Text Entry
##country_input = st.text_input("Enter your country")
##state_input = st.text_input("Enter your state")
##county_input = st.text_input("Enter your state's county")



# Disease.SH API


def get_dsh_data(location_country):
    url = f"https://disease.sh/v3/covid-19/countries/{location_country}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        confirmed_cases = data["cases"]
        deaths = data["deaths"]
        recovered = data["recovered"]
        return f"Confirmed COVID-19 cases in {location_country}: {confirmed_cases:,}\nConfirmed COVID-19 Deaths: {deaths:,}\nConfirmed COVID-19 Recovered: {recovered:,}"
    else:
        return "Unable to retrieve data"

location_country = st.text_input("Enter the name of your country:")
if location_country:
    st.write(get_dsh_data(location_country))
#location_country = input("Enter the name of your country: ")
#print(get_dsh_data(location_country))
#st.write(get_dsh_data(location_country))



def get_covid_data(location_state):
    url = f"https://disease.sh/v3/covid-19/states/{location_state}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        confirmed_cases = data["cases"]
        deaths = data["deaths"]
        recovered = data["recovered"]
        return f"Confirmed COVID-19 cases in {location_state}: {confirmed_cases:,}\nConfirmed COVID-19 Deaths: {deaths:,}\nConfirmed COVID-19 Recovered: {recovered:,}"
    else:
        return "Unable to retrieve Coronavirus data"

location_state = st.text_input("Enter the name of your U.S State:")
if location_state:
    st.write(get_covid_data(location_state))


#location_state = input("Enter the name of your state: ")
#print(get_covid_data(location_state))
#st.write(get_covid_data(location_state))


# County data is still giving us errors, let's come back to it later. - 03/20/2023

#def get_cdc_data(county):
#    url = f"https://data.cdc.gov/resource/3nnm-4jni.json{county}"
#    response = requests.get(url)
#    if response.status_code == 200:
#        data = response.json()
#        confirmed_cases = data["cases"]
#        deaths = data["deaths"]
#        recovered = data["recovered"]
#        return f"Confirmed cases in {county}: {confirmed_cases:,}\nDeaths: {deaths:,}\nRecovered: {recovered:,}"
#    else:
#        return "Unable to retrieve data"


#county = input("Enter the name of your county: ")
#print(get_cdc_data(county))
#st.write(get_cdc_data(county))


