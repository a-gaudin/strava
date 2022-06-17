import os
import pandas as pd
from typing import Union
from pathlib import Path

from utils.helper_functions import get_config
from data_extract.strava_api import StravaAPI

class Extract:
    def __init__(self) -> None:
        """ Init file paths """
        self.cfg = get_config()
        self.cfg_db = self.cfg.db.extract
        self.activities_db_path = Path(self.cfg_db.folder_path) / self.cfg_db.activities_file_name
        self.new_activities_db_path = Path(self.cfg_db.folder_path) / self.cfg_db.new_activities_file_name
    
    def __get_db_ids(self) -> Union[pd.DataFrame, None]:
        """ Get all activity ids stored in local db
        Returns:
            Union[pd.DataFrame, None]: local db ids or None
        """
        if self.activities_db_path.is_dir():
            df = pd.read_pickle(self.activities_db_path)
            return df['id']
        else:
            return None

    def __get_new_ids(self) -> Union[list, None]:
        """ Get the ids of the new activities, which are not stored in a local db
        Returns:
            Union[list, None]: ids of new activities or None
        """
        all_strava_activities_df = pd.json_normalize(StravaAPI().get_all_activities())
        all_strava_ids_df = all_strava_activities_df['id']
        all_db_ids_df = self.__get_db_ids()
        if all_db_ids_df:
            return list(set(all_strava_ids_df).difference(set(all_db_ids_df)))
        else:
            return None

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

    def save_new_activities(self) -> None:
        """ Save new activities as a pickle file.
        If no new activities, delete a potential old pickle file
        """
        new_ids = self.__get_new_ids()
        if new_ids:
            new_activities_json = self.__get_new_activities(new_ids)
            new_activities_df = pd.json_normalize(new_activities_json)
            new_activities_df.to_pickle(self.new_activities_db_path)
        else:
            try:
                self.new_activities_db_path.unlink() # unlink = remove file
            except OSError:
                pass