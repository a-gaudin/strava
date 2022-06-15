import os
import pandas as pd
import numpy as np
from typing import Union

import config
from extract.strava_api import StravaAPI

class Extract:
    def __init__(self) -> None:
        self.all_strava_activities_df = self.get_all_strava_activities()

    def get_new_activities(self) -> list:
        all_strava_ids_df = self.all_strava_activities_df['id']
        all_db_ids_df = self.get_db_ids()

        return list(set(all_strava_ids_df['id']) & set(all_db_ids_df['id']))

    def get_all_strava_ids(self) -> pd.DataFrame:
        return self.all_strava_activities_df['id']

    def get_all_strava_activities(self) -> pd.DataFrame:
        """ Get all Strava activities
        Returns:
            (pd.DataFrame): all Strava activities
        """
        activities_json = StravaAPI().get_all_activities()
        activities_df = pd.json_normalize(activities_json)
        return activities_df[['id', 'name', 'distance', 'moving_time', 'elapsed_time',
                                'total_elevation_gain', 'type', 'start_date', 'average_speed']]

    def get_db_ids(self) -> Union[pd.DataFrame, None]:
        """ Get all activity ids stored  in local db
        Returns:
            Union[pd.DataFrame, None]: local db ids or None
        """
        if os.path.isfile(config.db_file_path):
            df = pd.read_pickle(config.db_file_path)
            return df['id']
        else:
            return None

    def get_activity(self) -> pd.DataFrame:
         """ Returns the activity dataframe with information about training load """
        for id in df['id']]:
            df['perceived_exertion'] = [x['perceived_exertion'] for x in load_list]
            df['note'] = [x['note'] for x in load_list]

            df['load'] = df['moving_time'] * df['perceived_exertion']
        return df
        activity_json = StravaAPI().get_activity(id) 
