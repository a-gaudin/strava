import pandas as pd
from pathlib import Path

import utils.helper_functions as help_fn
import utils.convert as convert

class CreateInjuries:
    def __init__(self) -> None:
        """ Get transform config data """
        self.cfg = help_fn.get_config()

        self.cfg_db = self.cfg.db.transform
        self.db_folder_path = Path(self.cfg_db.folder_path)
        self.injuries_db_path = self.db_folder_path / self.cfg_db.injuries_file_name

        self.cfg_injuries = self.cfg.df.transform.injuries
        self.notes_start_date = self.cfg_injuries.notes_start_date
        self.sports = self.cfg_injuries.sports
    
    def __add_cumulative_injuries(self, df: pd.DataFrame) -> pd.DataFrame:
        df.set_index(df['start_date'], inplace=True)
        df['injury_last_1W'] = df["injury_score"].rolling('7D').sum()

        return df

    def create_injuries_db(self, df: pd.DataFrame) -> None:
        df = df[(df.iloc[:, 7] > self.notes_start_date)] # filter out older activities without injury notes
        df = df[df.iloc[:, 6].isin(self.sports)]
        df = self.__add_cumulative_injuries(df)

        df.to_pickle(self.injuries_db_path)

        print(f'Activities shape: {df.shape}')
        pd.set_option('display.max_columns', None)
        print(df.head(5))