import requests
import urllib3

##API code for 'CovidActNow API' (Fetching Local COVID Data)
API_KEY = "c4edd54144b943c68a637a1b64194c0c"
## --> Command Prompt/Terminal --> pip install requests
BASE_URL_STATE ="https://api.covidactnow.org/v2/states.json"
BASE_URL_COUNTY ="https://api.covidactnow.org/v2/counties.json"

state = input("Please enter a state: ")
county = input("Please enter a county in the state: ")

request_url = f"{BASE_URL_STATE}?appid={API_KEY}&q={state}"
request_url = f"{BASE_URL_COUNTY}?appid={API_KEY}&q={county}"
response = requests.get(request_url)

if response.status_code == 200:
    data = response.json()

else:
    print("An error has occured. Please try the software again. ")


