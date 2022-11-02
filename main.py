import time
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
from urllib3.util import url
mpl.use("agg")

from statedata import us_state_to_abbrev, us_state_list
from countydata import us_state_county
#from countrydata import country_list

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



_ENABLE_PROFILING = False

if _ENABLE_PROFILING:
    import cProfile, pstats, io
    from pstats import SortKey
    pr = cProfile.Profile()
    pr.enable()

today = date.today()


##URL for webscraping National U.S COVID Data
#html_text = requests.get('https://www.worldometers.info/coronavirus/country/us/')
#webpage = urlopen(response).read()
#html = soup(webpage, "html.parser")
#webscrapenum = soup.findall('li', class_ = '#maincounter-number')
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
#response = Request(url, headers = headers)



#Streamlit Main Webpage Header and Info
st.title('COVID-19 Utility Web Application')
st.markdown("""
* **Data sources: COVID Data API(s):** [COVID-Act-Now.com](https://apidocs.covidactnow.org/), [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19), [New York Times](https://github.com/nytimes/covid-19-data)""")


st.write("""
This webpage uses COVID-19 Data API to gather accurate data and present it in one place.

**This is an early version of the program, please do not take COVID data presented here as an accurate reflection.**
***
""")


sidebar_selection = st.sidebar.radio(
    'Select location data to display:',
    ['Show All', 'Show State', 'Show County', 'Show U.S National'],
)

sidebar_selection = st.sidebar.radio(
    'Select which data source to display:',
    ['Show All Sources', 'Show COVIDActNow Data ', 'Show Johns Hopkins University Data', 'Show New York Times Data'],
)


st.header('Enter corresponding information into your console/terminal')

st.subheader('COVID Data for State and County:')
selected_state = st.sidebar.selectbox('State', dict())
selected_county = st.sidebar.selectbox('County', dict())





#selected_county = st.sidebar.selectbox('Country', dict())

#st.dataframe(df_selected_sector)
#df = load_data()
#sorted_sector_unique = sorted( df['Total U.S COVID Cases']).unique()
#sorted_sector_unique = sorted( df['Total U.S COVID Deaths']).unique()
#sorted_sector_unique = sorted( df['Total U.S COVID Recovered Cases']).unique()
#selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique)

# Streamlit Webpage Text Entry
#state_input = st.text_input("Enter your state")
#county_input = st.text_input("Enter your state's county")


##State COVID Data **needs fixing**
state_url = "https://api.covidactnow.org/v2/states.json?apiKey=c4edd54144b943c68a637a1b64194c0c"
response = requests.get(state_url)
data = response.json()
#API_KEY = "c4edd54144b943c68a637a1b64194c0c"
states = [x["state"] for x in data]
cases = [x["actuals"]["cases"] for x in data]
deaths = [x["actuals"]["deaths"] for x in data]



##County-level COVID Data **needs fixing**
county_url = "https://api.covidactnow.org/v2/counties.json?apiKey=c4edd54144b943c68a637a1b64194c0c"
response = requests.get(county_url)
data = response.json()
#API_KEY = "c4edd54144b943c68a637a1b64194c0c"
counties = [x["county"] for x in data]
cases = [x["actuals"]["cases"] for x in data]
deaths = [x["actuals"]["deaths"] for x in data]

print(cases)
print(deaths)
#counties = [x["county"] for x in data]
#cases = [x["actuals"]["cases"] for x in data]
#print(cases)



countries = [x["country"] for x in data]
cases = [x["actuals"]["cases"] for x in data]
deaths = [x["actuals"]["deaths"] for x in data]

# Johns Hopkins COVID Data API
def get_data():
    US_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
    US_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
    confirmed = pd.read_csv(US_confirmed)
    usdeaths = pd.read_csv(US_deaths)
    return confirmed, usdeaths
confirmed, usdeaths = get_data()

FIPSs = confirmed.groupby(['Province_State', 'Admin2']).FIPS.unique().apply(pd.Series).reset_index()
FIPSs.columns = ['State', 'County', 'FIPS']
FIPSs['FIPS'].fillna(0, inplace = True)
FIPSs['FIPS'] = FIPSs.FIPS.astype(int).astype(str).str.zfill(5)

# New York Times COVID Data API
def get_data():
    # U.S Death Data
    USA_deaths = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    usadeaths = pd.read_csv(USA_deaths)
    # U.S COVID Case Data
    USA_cases = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    usacases = pd.read_csv(USA_cases)
    # U.S State COVID Death Data
    State_deaths = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
    statedeaths = pd.read_csv(State_deaths)
    # U.S State COVID Case Data
    State_cases = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
    statecases = pd.read_csv(State_cases)
    # U.S County COVID Death Data
    County_deaths = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
    countydeaths = pd.read_csv(County_deaths)
    # U.S County COVID Case Data
    County_cases = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
    countycases = pd.read_csv(County_cases)

    return usadeaths, usacases, statedeaths, statecases, countydeaths, countycases
usadeaths, usacases, statedeaths, statecases, countydeaths, countycases = get_data()

# CovidActNow API Dict 1-4
dictionary_1 = dict(zip(states, cases))
dictionary_2 = dict(zip(counties, cases))
dictionary_3 = dict(zip(states, deaths))
dictionary_4 = dict(zip(counties, deaths))

# Johns Hopkins API Dict 5-8
dictionary_5 = dict(zip(states, confirmed))
dictionary_6 = dict(zip(counties, confirmed))
dictionary_7 = dict(zip(states, usdeaths))
dictionary_8 = dict(zip(counties, usdeaths))

# New York Times COVID Data API Dict 9 - 13
#dictionary_9 = dict(zip(countries, usadeaths))
dictionary_10 = dict(zip(states, statedeaths))
dictionary_11 = dict(zip(counties, countydeaths))
dictionary_12 = dict(zip(states, statecases))
dictionary_13 = dict(zip(counties, countycases))
#dictionary_12 = dict(zip(countries, )





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

#while (inp == False):
    #try:
        #state = input("Please enter a state: ")
        #state = state.lower()
        #state = state.title()
        #state_key = us_state_list[state]
        #print(state_key)
        #inp = True
    #except:
        #print("Try again")




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


#while (inp == False):
    #try:
        #country = input("Please enter a country: ")
        #country = country.lower()
        #country = country.title()
        #country_key = [country_list][country]
        #print(country_key)
        #inp = True
    #except:
        #print("Try again")


#main console-terminal print

#COVIDActNow Data print
print("There are " + str(dictionary_1[state_key]) + " total confirmed COVID-19 deaths in " + state + " according to the [COVID Act Now API]")
print("There are " + str(dictionary_2[county_key]) + " total confirmed COVID-19 deaths in " + county + " according to the [COVID Act Now API]")
print("There are " + str(dictionary_3[state_key]) + " total COVID-19 cases in " + state + " according to the [COVID Act Now API]")
print("There are " + str(dictionary_4[county_key]) + " total COVID-19 cases in " + county + " according to the [COVID Act Now API]")


#Johns Hopkins University Data print
print("There are " + str(dictionary_5[state_key]) + " total confirmed COVID-19 cases in " + state + " according to [Johns Hopkins University]")
print("There are " + str(dictionary_6[county_key]) + " total confirmed COVID-19 deaths in " + county + " according to [Johns Hopkins University]")
print("There are " + str(dictionary_7[state_key]) + " total confirmed COVID-19 deaths in " + state + " according to [Johns Hopkins University]")
print("There are " + str(dictionary_8[county_key]) + " total confirmed COVID-19 deaths in " + county + " according to [Johns Hopkins University]")

#New York Times Data print

#print("There are " + str(dictionary_9[country_key]) + " total confirmed COVID-19 deaths in " + country + " according to [New York Times]")
print("There are " + str(dictionary_10[state_key]) + " total confirmed COVID-19 deaths in " + state + " according to [New York Times]")
print("There are " + str(dictionary_11[county_key]) + " total confirmed COVID-19 deaths in " + county + " according to [New York Times]")
print("There are " + str(dictionary_12[state_key]) + " total confirmed COVID-19 cases in " + state + " according to [New York Times]")
print("There are " + str(dictionary_13[county_key]) + " total confirmed COVID-19 cases in " + county + " according to [New York Times]")


#streamlit webpage print
# COVID Act Now API
st.write("There are " + str(dictionary_1[state_key]) + " total confirmed COVID-19 deaths in " + state + " according to the [COVID Act Now API](https://apidocs.covidactnow.org/)")
st.write("There are " + str(dictionary_2[county_key]) + " total confirmed COVID-19 deaths in " + county + " according to the [COVID Act Now API](https://apidocs.covidactnow.org/)")
st.write("There are " + str(dictionary_3[state_key]) + " total COVID-19 cases in " + state + " according to the [COVID Act Now API](https://apidocs.covidactnow.org/)")
st.write("There are " + str(dictionary_4[county_key]) + " total COVID-19 cases in " + county + " according to the [COVID Act Now API](https://apidocs.covidactnow.org/)")

# Johns Hopkins University API
st.write("There are " + str(dictionary_5[state_key]) + " total confirmed COVID-19 cases in " + state + " according to [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19)")
st.write("There are " + str(dictionary_6[county_key]) + " total confirmed COVID-19 cases in " + county + " according to [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19)")
st.write("There are " + str(dictionary_7[state_key]) + " total confirmed COVID-19 deaths in " + state + " according to [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19)")
st.write("There are " + str(dictionary_8[county_key]) + " total confirmed COVID-19 deaths in " + county + " according to [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19)")

# New York Times API
#st.write("There are " + str(dictionary_9[country_key]) + " total confirmed COVID-19 deaths in " + country + " according to [New York Times]")
st.write("There are " + str(dictionary_10[state_key]) + " total confirmed COVID-19 deaths in " + state + " according to [New York Times]")
st.write("There are " + str(dictionary_11[county_key]) + " total confirmed COVID-19 deaths in " + county + " according to [New York Times]")
st.write("There are " + str(dictionary_12[state_key]) + " total confirmed COVID-19 cases in " + state + " according to [New York Times]")
st.write("There are " + str(dictionary_13[county_key]) + " total confirmed COVID-19 cases in " + county + " according to [New York Times]")



_lock = RendererAgg.lock
fig = Figure(figsize=(12, 8))
with _lock:
    if len(county) < 6:
        fig.suptitle(
            'Current COVID-19 Data for your selected location ' + ', '.join(map(str, county)) + ' county (' + str(today) + ')')
    else:
        fig.suptitle('Current COVID-19 Data for your selected location (' + str(today) + ')')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    st.pyplot(fig)

_lock = RendererAgg.lock
fig = Figure(figsize=(12, 8))
with _lock:
    if len(state) < 6:
        fig.suptitle(
            'Current COVID-19 Data for your selected location ' + ', '.join(map(str, state)) + ' state (' + str(today) + ')')
    else:
        fig.suptitle('Current COVID-19 Data for your selected location (' + str(today) + ')')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    st.pyplot(fig)



    import streamlit.components.v1 as components
    if len(county)<=3:
        for C in county:
            st.text(C)
            f = FIPSs[FIPSs.County == C].FIPS.values[0]
            components.iframe("https://covidactnow.org/embed/us/county/"+f, width=350, height=365, scrolling=False)

    import streamlit.components.v1 as components
    if len(state)<=3:
        for S in state:
            st.text(S)
            f = FIPSs[FIPSs.State == S].FIPS.values[0]
            components.iframe("https://covidactnow.org/embed/us/state/"+f, width=350, height=365, scrolling=False)




# Streamlit Sidebar Description Info
with st.sidebar.expander("Click here to learn more about the COVID-19 Utility (Web-Application)"):
    st.markdown(f"""
    The COVID-19 Utility Web Application was developed to track and monitor data regarding the Coronavirus Pandemic to better understand the data surrounding it in an easy-to-use, friendly manner.
    
    COVID Data traced from:
    [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19), [*COVIDActNow Org*](https://covidactnow.org/)
    
    *COVID-19 Utility (WebApp) data last updated on {str(today)}.*  
    """)

st.write("""

**This is an early version of the program, please do not take COVID data presented here as an accurate reflection.**
***

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
[**COVID-19 Common Questions**](https://www.fda.gov/emergency-preparedness-and-response/coronavirus-disease-2019-covid-19/covid-19-frequently-asked-questions)""")




t1, t2 = st.columns(2)
#with t1:
    #st.markdown('# COVID-19 Utility Data Dashboard')

with t2:
    st.write("")
    st.write("")
    st.write("""
    **Built by Arian Kharazmi**
    """)



# Stat Sorter
if _ENABLE_PROFILING:
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    ts = int(time.time())
    with open(f"perf_{ts}.txt", "w") as f:
        f.write(s.getvalue())

# end