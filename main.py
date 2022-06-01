def get_access_token(params):
    """ Returns an access token from Strava """
    auth_url = "https://www.strava.com/oauth/token"
    res = requests.post(auth_url, data=params, verify=False)
    return res.json()['access_token']

def get_activities(access_token, params):
    """ Returns a dataframe of Strava activities """
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': 'Bearer ' + access_token}
    activities_json = requests.get(activites_url, headers=header, params=params).json()
    activities_df = pd.json_normalize(activities_json)
    activities_df = activities_df[['name', 'distance', 'moving_time', 'elapsed_time', 'total_elevation_gain', 'type', 'start_date', 'average_speed', 'max_speed']]
    return activities_df

def change_units(activities_df):
    activities_df["distance"] = activities_df["distance"] / 1000
    activities_df["elapsed_time"] = pd.to_datetime(activities_df["elapsed_time"], unit='s')
    activities_df["average_speed"] = activities_df["average_speed"] * 3.6
    return activities_df

def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    access_token = get_access_token(config.token_request_params)
    activities_df = get_activities(access_token, config.activities_request_params)
    activities_df = change_units(activities_df)
    
if __name__ == "__main__":
    import config
    import requests
    import urllib3
    import pandas as pd

    main()