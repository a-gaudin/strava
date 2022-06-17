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
        self.db_folder_path = Path(self.cfg_db.folder_path)
        self.activities_db_path = self.db_folder_path / self.cfg_db.activities_file_name
        self.new_activities_db_path = self.db_folder_path / self.cfg_db.new_activities_file_name
    
    def __get_local_ids(self) -> Union[pd.DataFrame, None]:
        """ Get all activity ids stored in local db
        Returns:
            Union[pd.DataFrame, None]: local db ids or None
        """
        if self.activities_db_path.is_file():
            df = pd.read_pickle(self.activities_db_path)
            return df['id']
        else:
            return None

    def __get_new_ids(self) -> list:
        """ Get the ids of the new activities, which are not stored in a local db
        Returns:
            (list): ids of new activities
        """
        all_strava_activities_df = pd.json_normalize(StravaAPI().get_all_activities())
        all_strava_ids_df = all_strava_activities_df['id']
        all_local_ids_df = self.__get_local_ids()
        return (
            list(set(all_strava_ids_df).difference(set(all_local_ids_df)))
            if all_local_ids_df
            else list(set(all_strava_ids_df)) )
    
    def __get_new_activities(self, ids: list) -> str:
        """ Get the data of the new activities, which are not stored in a local db
        Args
            ids (list): ids to search for
        Results
            all_new_activities (str): new activities as a JSON string
        """
        all_new_activities = []
        for id in ids:
            new_activity = StravaAPI().get_activity(id) 
            print(f'Returned data for activity {id}')
            all_new_activities.append(new_activity)
        return all_new_activities

    def update_activities_db(self) -> None:
        """ Save new activities as a pickle file.
        If no new activities, delete a potential old pickle file
        """
        self.db_folder_path.mkdir(parents=True, exist_ok=True)

        new_ids = self.__get_new_ids()
        if new_ids:
            new_activities_json = self.__get_new_activities(new_ids)
            new_activities_df = pd.json_normalize(new_activities_json)

            if self.activities_db_path.is_file():
                local_activities_df = pd.read_pickle(self.activities_db_path)  
                activities_df = pd.concat([local_activities_df, new_activities_df])
                activities_df.to_pickle(self.activities_db_path)
            else:
                new_activities_df.to_pickle(self.activities_db_path)

      