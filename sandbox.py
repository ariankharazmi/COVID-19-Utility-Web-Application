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
import requests

import streamlit as st
import requests

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
