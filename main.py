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
* **Data sources: COVID Data API(s):** [Centers for Disease Control](https://apidocs.covidactnow.org/), [Worldometers](https://github.com/CSSEGISandData/COVID-19), [New York Times](https://github.com/nytimes/covid-19-data)""")


st.write("""
This webpage uses COVID-19 Data from different API sources to gather accurate data and present it in one place.

**This is an early version of the program, please do not take COVID-19 data presented here as an accurate reflection.**
***
""")


#sidebar_selection = st.sidebar.radio(
#    'Select location data to display:',
#    ['Show All', 'Show Country', 'Show U.S State', 'Show U.S County'],
#)
#sidebar_selection = st.sidebar.radio(
#    'Select which data source to display:',
#    ['Show All Sources', 'Show CDC Data ', 'Show Worldometers Data', 'Show New York Times Data'],
#)


st.subheader('Please enter corresponding information into the fields below to retrieve Coronavirus data.')



#selected_country = st.sidebar.selectbox('Country', dict())
#selected_state = st.sidebar.selectbox('State', dict())
#selected_county = st.sidebar.selectbox('County', dict())


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
        st.subheader(f"COVID-19 Data for {location_country}")
        st.write("- Confirmed cases: {:,.0f}".format(confirmed_cases))
        st.write("- Confirmed deaths: {:,.0f}".format(deaths))
        st.write("- Confirmed recoveries: {:,.0f}".format(recovered))
        return None
    else:
        st.write(f"Unable to retrieve Coronavirus data for {location_country}")

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
        st.subheader(f"COVID-19 Data for {location_state}")
        st.write("- Confirmed cases: {:,.0f}".format(confirmed_cases))
        st.write("- Confirmed deaths: {:,.0f}".format(deaths))
        st.write("- Presumed recoveries**: {:,.0f}".format(recovered))
        return None
    else:
        st.write(f"Unable to retrieve Coronavirus data for {location_state}")

location_state = st.text_input("Enter the name of your U.S State:")
if location_state:
    st.write(get_covid_data(location_state))


#location_state = input("Enter the name of your state: ")
#print(get_covid_data(location_state))
#st.write(get_covid_data(location_state))


# County data is still giving us errors, let's come back to it later. - 03/20/2023
#def get_actnow_data(location_county):
#    url = f"https://api.covidactnow.org/v2/counties.json?apiKey=c4edd54144b943c68a637a1b64194c0c{location_county}"
#    response = requests.get(url)
#    if response.status_code == 200:
#        data = response.json()
#        confirmed_cases = data["cases"]
#        deaths = data["deaths"]
#        recovered = data["recovered"]
#        return f"Confirmed cases in {location_county}: {confirmed_cases:,}\nDeaths: {deaths:,}\nRecovered: {recovered:,}"
#    else:
#        return "Unable to retrieve Coronavirus data for {location_county}"


#location_county = input("Enter the name of your county: ")
#if location_county:
#    st.write(get_actnow_data(location_county))



with st.sidebar.expander("Click here to learn more about the COVID-19 Utility (Web-Application)"):
    st.markdown(f"""
    The COVID-19 Utility Web Application was developed to track and monitor data regarding the Coronavirus Pandemic to better understand the data surrounding it in an easy-to-use, friendly manner.

    COVID Data traced from:
    [Disease.SH](https://github.com/CSSEGISandData/COVID-19), [*COVIDActNow Org*](https://covidactnow.org/), [New York Times](https://github.com/nytimes/covid-19-data)

    *COVID-19 Utility (Web Application) data last updated on {str(today)}.*  
    """)



st.write("""
* **Quick Web Links**
[**CDC Coronavirus Statistics Website**](https://www.cdc.gov/coronavirus/2019-nCoV/index.html)""")
st.write("""
[**New York Times Coronavirus Statistics Website**](https://www.nytimes.com/interactive/2021/us/covid-cases.html)""")
st.write("""
[**Do I have COVID-19?**](https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.html)""")
st.write("""
[**What should I do if I have COVID-19?**](https://www.cdc.gov/coronavirus/2019-ncov/if-you-are-sick/steps-when-sick.html)""")
st.write("""
[**Where can I get masks, vaccines, and tests?**](https://www.covid.gov/)""")
st.write("""
[**Can I get a flu shot and a COVID-19 Vaccine at the same time?**](https://www.cdc.gov/flu/prevent/coadministration.htm)""")
st.write("""
[**COVID-19 Common Questions**](https://www.fda.gov/emergency-preparedness-and-response/coronavirus-disease-2019-covid-19/covid-19-frequently-asked-questions)""")

t1, t2 = st.columns(2)
# with t1:
#
# st.markdown('# COVID-19 Utility Data Dashboard')

with t2:
    st.write("")
    st.write("")
    st.write("""
    **Built by Arian Kharazmi**
    """)
