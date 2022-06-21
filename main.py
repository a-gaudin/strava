import pandas as pd
from pathlib import Path

from utils.helper_functions import get_config

from data_extract.extract import Extract
from data_transform.activities import CreateActivities
from data_transform.summary import SummarizeActivities

def main() -> None:
    # Extract().update_strava_activities_db()

    cfg = get_config()

    # strava_activities_db_filename = Path(cfg.db.extract.folder_path) / cfg.db.extract.activities_file_name
    # strava_activities_df = pd.read_pickle(strava_activities_db_filename)

    # CreateActivities().create_activities_db(strava_activities_df)

    activities_db_filename = Path(cfg.db.transform.folder_path) / cfg.db.transform.activities_file_name
    activities_df = pd.read_pickle(activities_db_filename)

    SummarizeActivities().create_summary_db(activities_df)

    print('hello')

if __name__ == "__main__":
    main()