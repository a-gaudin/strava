import config
import requests
import urllib3
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_access_token(params):
    """ Returns an access token from Strava """
    auth_url = 'https://www.strava.com/oauth/token'
    res = requests.post(auth_url, data=params, verify=False)
    return res.json()['access_token']

def get_activity(id):
    """ Returns a Strava activity's description """
    access_token = get_access_token(config.token_request_params)
    
    activity_url = 'https://www.strava.com/api/v3/activities/' + str(id)
    header = {'Authorization': 'Bearer ' + access_token}
    params = {
        'include_all_efforts': False
    }

    activity_json = requests.get(activity_url, headers=header, params=params).json()

    return activity_json

def get_activities():
    """ Returns a dataframe of all Strava activities """
    access_token = get_access_token(config.token_request_params)

    activities_url = 'https://www.strava.com/api/v3/athlete/activities'
    header = {'Authorization': 'Bearer ' + access_token}

    run_new_request = True
    page = 1
    activities_json= []

    while run_new_request == True:
        params = {
            'per_page': config.request_batch_size,
            'page': page
        }
        new_activities_json = requests.get(activities_url, headers=header, params=params).json()
        activities_json += new_activities_json
        page += 1

        if len(new_activities_json) < config.request_batch_size:
            run_new_request = False

    return pd.json_normalize(activities_json)