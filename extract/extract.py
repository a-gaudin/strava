import os
import pandas as pd
from typing import Union

import config
from extract.strava_api import StravaAPI

class Extract:
    def __init__(self) -> None:
        self.save_new_activities()
    
    def __get_db_ids(self) -> Union[pd.DataFrame, None]:
        """ Get all activity ids stored  in local db
        Returns:
            Union[pd.DataFrame, None]: local db ids or None
        """
        file_path = config.db_folder + config.db_activities_filename
        if os.path.isfile(file_path):
            df = pd.read_pickle(file_path)
            return df['id']
        else:
            return None

    def __get_new_ids(self) -> list:
        """ Get the ids of the new activities, which are not stored in a local db
        Returns:
            (list): ids of new activities """
        all_strava_activities_df = pd.json_normalize(StravaAPI().get_all_activities())
        all_strava_ids_df = all_strava_activities_df['id']
        all_db_ids_df = self.__get_db_ids()
        return list(set(all_strava_ids_df['id']) & set(all_db_ids_df['id']))

    def __get_new_activities(self, ids: list) -> str:
        """ Get the data of the new activities, which are not stored in a local db
        Args
            ids (list): ids to search for
        Results
            all_new_activities (str): new activities as a JSON string
        """
        all_new_activities = ''
        for id in ids:
            new_activity = StravaAPI().get_activity(id) 
            print(f'Returned data for activity {id}')
            all_new_activities += new_activity
        return all_new_activities
    
    def save_new_activities(self):
        new_ids = self.__get_new_ids()
        new_activities = self.__get_new_activities(new_ids)
        file_path = config.db_folder + config.db_new_activities_filename
        new_activities.to_pickle(file_path)
