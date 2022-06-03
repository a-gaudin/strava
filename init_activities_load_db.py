import pandas as pd
import strava_api

def get_load(id):
    """ Returns a dictionary with rate of perceived exertion and description
        (that may contain soreness/pain information) """
    activity_json = strava_api.get_activity(id)
    perceived_exertion = activity_json['perceived_exertion']
    description = activity_json['description']

    return {perceived_exertion: perceived_exertion, description: description}

def add_load(activities_df):
    """ Adds the training load information to the activities dataframe """
    load_list = [get_load(id) for id in activities_df['id']]
    print(load_list)

def main():
    activities_df = pd.read_pickle("./db/activities.pkl")
    activities_load_df = add_load(activities_df)

    pd.set_option('display.max_columns', None)
    # print(activities_load_df.head(10))

if __name__ == "__main__":
    main()