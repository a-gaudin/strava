import pandas as pd
import strava_api

def get_load(id):
    """ Returns a dictionary with rates of perceived exertion and notes
        (that may contain soreness/pain information) """
    activity_json = strava_api.get_activity(id) 
    perceived_exertion = activity_json['perceived_exertion'] if 'perceived_exertion' in activity_json else float("NaN")
    note = activity_json['private_note'] if 'private_note' in activity_json else ''
    return {'perceived_exertion': perceived_exertion, 'note': note}

def add_load(activities_df):
    """ Adds the training load information to the activities dataframe """
    load_list = [get_load(id) for id in activities_df['id']]
    activities_df['perceived_exertion'] = [x['perceived_exertion'] for x in load_list]
    activities_df['note'] = [x['note'] for x in load_list]
    return activities_df

def main():
    activities_df = pd.read_pickle("./db/activities.pkl")
    activities_df = add_load(activities_df)
    # activities_df = note_to_soreness(activities_df)

    pd.set_option('display.max_columns', None)
    print(activities_df.head(10))

if __name__ == "__main__":
    main()