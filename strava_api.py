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

def get_activities():
    """ Returns a dataframe of Strava activities """
    access_token = get_access_token(config.token_request_params)

    activites_url = 'https://www.strava.com/api/v3/athlete/activities'
    header = {'Authorization': 'Bearer ' + access_token}

    run_new_request = True
    page = 1
    activities_json= []

    while run_new_request == True:
        params = {
            'per_page': config.request_batch_size,
            'page': page
        }
        new_activities_json = requests.get(activites_url, headers=header, params=params).json()
        activities_json += new_activities_json
        page += 1

        if len(new_activities_json) < config.request_batch_size:
            run_new_request = False

    activities_df = pd.json_normalize(activities_json)
    return activities_df[['name', 'distance', 'moving_time', 'elapsed_time',
                        'total_elevation_gain', 'type', 'start_date', 'average_speed']]