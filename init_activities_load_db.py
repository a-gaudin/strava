import pandas as pd
import strava_api
    
def main():
    activities_df = pd.read_pickle("./db/activities.pkl")
    # activities_load_df = add_training_load(activities_df)

    pd.set_option('display.max_columns', None)
    # print(activities_load_df.head(10))

if __name__ == "__main__":
    main()