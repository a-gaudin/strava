import pandas as pd
from pathlib import Path

from utils.helper_functions import get_config

from data_extract.extract import Extract
from data_transform.transform import Transform

def main() -> None:
    Extract().update_strava_activities_db()

    cfg = get_config()
    strava_activities_db_filename = Path(cfg.db.extract.folder_path) / cfg.db.activities_file_name
    strava_activities_df = pd.read_pickle(strava_activities_db_filename)  
    Transform().create_activities_db(strava_activities_df)
    
    print('hello')

if __name__ == "__main__":
    main()