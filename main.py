import config
import requests
import urllib3
import pandas as pd
import numpy as np

def get_access_token(params):
    """ Returns an access token from Strava """
    auth_url = "https://www.strava.com/oauth/token"
    res = requests.post(auth_url, data=params, verify=False)
    return res.json()['access_token']

def get_activities(access_token):
    """ Returns a dataframe of Strava activities """
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
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
    return activities_df[['name', 'distance', 'moving_time', 'elapsed_time', 'total_elevation_gain', 'type', 'start_date', 'average_speed']]

def change_units(df):
    """ Converts distances to km and speeds to km/h """
    df.rename(columns = {'average_speed':'moving_speed', 'total_elevation_gain':'elevation_gain'}, inplace = True)
    df["distance"] = df["distance"] / 1000
    df["moving_speed"] = df["moving_speed"] * 3.6
    df["start_date"] = pd.to_datetime(df["start_date"])
    return df

def add_new_columns(df):
    df["elapsed_time_hhmmss"] = pd.to_datetime(df["elapsed_time"], unit='s').dt.time
    df["speed"] = df["distance"] / (df["elapsed_time"] / 3600)
    df["grade_adjusted_speed"] = (df["distance"] + (df["elevation_gain"] / 1000)) / (df["elapsed_time"] / 3600)
    df["average_slope"] = (df["elevation_gain"] / (df["distance"] / 2 * 1000)) * 100
    df["month"] = df["start_date"].dt.to_period('M')
    df["year"] = df["start_date"].dt.to_period('Y')
    return df

def get_summary(df):
    """ Returns a pivot table dataframe that summarizes the activities """
    pivot_table = pd.pivot_table(df, values=['distance', 'elapsed_time', 'elevation_gain'],
                                index=['month'], columns=['type'], aggfunc=np.sum, fill_value=0)
    #pivot_table = pivot_table.sort_values(by="month", ascending=False).index
    return pivot_table #[["Run", "Bike"]]

def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    access_token = get_access_token(config.token_request_params)

    activities_df = get_activities(access_token)
    activities_df = change_units(activities_df)
    activities_df = add_new_columns(activities_df)

    pd.set_option('display.max_columns', None)
    print(activities_df.shape)
    print(activities_df.head())

    summary_df = get_summary(activities_df)
    print(summary_df.head())
    
if __name__ == "__main__":
    main()