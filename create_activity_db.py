from strava_api import StravaAPI
import pandas as pd

def change_units(df):
    """ Converts distances to km and speeds to km/h """
    df.rename(columns = {'average_speed':'moving_speed', 
                        'total_elevation_gain':'elevation_gain'}, inplace = True)
    df["distance"] = df["distance"] / 1000
    df["moving_speed"] = df["moving_speed"] * 3.6
    df["start_date"] = pd.to_datetime(df["start_date"])
    return df

def add_new_columns(df):
    df["elapsed_time_hhmmss"] = pd.to_datetime(df["elapsed_time"], unit='s').dt.time
    df["speed"] = df["distance"] / (df["elapsed_time"] / 3600)
    df["grade_adjusted_speed"] = (df["distance"] + (df["elevation_gain"] / 1000)) / (df["elapsed_time"] / 3600)
    df["average_slope"] = df["elevation_gain"] / (df["distance"] / 2 * 1000)
    df["moving_%"] = df["moving_time"] / df["elapsed_time"]
    df["month"] = df["start_date"].dt.to_period('M')
    df["year"] = df["start_date"].dt.to_period('Y')
    return df

def main():
    activities_json = StravaAPI().get_all_activities()
    activities_df = pd.json_normalize(activities_json)
    activities_df = activities_df[['id', 'name', 'distance', 'moving_time', 'elapsed_time',
                                'total_elevation_gain', 'type', 'start_date', 'average_speed']]
    activities_df = change_units(activities_df)
    activities_df = add_new_columns(activities_df)

    activities_df.to_pickle('./db/activity.pkl')

    print(activities_df.shape)
    print(activities_df.head())
    print('Saved ./db/activity.pkl')
    
if __name__ == "__main__":
    main()