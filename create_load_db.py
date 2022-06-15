import pandas as pd
from strava_api import StravaAPI

def get_load(id):
    """ Returns a dictionary with rates of perceived exertion and notes
        (that may contain soreness/pain information) """
    activity_json = StravaAPI().get_activity(id) 
    print(f'Returned data for activity {id}')
    perceived_exertion = activity_json['perceived_exertion'] if 'perceived_exertion' in activity_json else float("NaN")
    note = activity_json['private_note'] if 'private_note' in activity_json else ''
    return {'perceived_exertion': perceived_exertion, 'note': note}

def add_load(df):
    """ Returns the activity dataframe with information about training load """
    load_list = [get_load(id) for id in df['id']]
    df['perceived_exertion'] = [x['perceived_exertion'] for x in load_list]
    df['note'] = [x['note'] for x in load_list]

    df['load'] = df['moving_time'] * df['perceived_exertion']
    return df

def main():
    activities_df = pd.read_pickle('./db/activity.pkl')
    activities_df = add_load(activities_df)

    activities_df.to_pickle('./db/load.pkl')

    pd.set_option('display.max_columns', None)
    print(activities_df.shape)
    print(activities_df.head())

if __name__ == '__main__':
    main()