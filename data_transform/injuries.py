import pandas as pd
from pathlib import Path

import utils.helper_functions as help_fn

class CreateInjuries:
    def __init__(self) -> None:
        """ Get transform config data """
        self.cfg = help_fn.get_config()

        self.cfg_db = self.cfg.db.transform
        self.db_folder_path = Path(self.cfg_db.folder_path)
        self.injuries_db_path = self.db_folder_path / self.cfg_db.injuries_file_name

        self.cfg_injuries = self.cfg.df.transform.injuries
        self.notes_start_date = '10/09/2021'
        self.sports = ['Run']
        self.rolling_features = [
                {'reference': 'injury_score', 'column_name': 'injury_last_week', 'days': 7},
                {'reference': 'injury_score', 'column_name': 'injury_last_month', 'days': 30},
                {'reference': 'load', 'column_name': 'load_last_week', 'days': 7},
                {'reference': 'load', 'column_name': 'load_last_month', 'days': 30}
            ]
    
    def __add_cumulative_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Add cumulative injury and training load to injuries df
        Args:
            df (pd.DataFrame): injuries
        Return
            df (pd.DataFrame): injuries with cumulative injuries data and cumulative training load data
        """
        df.set_index(df["start_date"], inplace=True)
        for el in self.rolling_features:
            window = str(el.days) + 'D'
            df[el.column_name] = df[el.reference].rolling(window).sum()
        return df

    def create_injuries_db(self, df: pd.DataFrame) -> None:
        """" Save an activity database with rolling injury related metrics
        Args:
            df (pd.DataFrame): activities without rolling injury related metrics
        """
        df = df[(df["start_date"] > self.notes_start_date)] # filter out older activities without injury notes
        df = df[df["type"].isin(self.sports)]
        df = self.__add_cumulative_features(df)

        df.to_pickle(self.injuries_db_path)

        print(f'Activities shape: {df.shape}')
        pd.set_option('display.max_columns', None)
        print(df.head(5))