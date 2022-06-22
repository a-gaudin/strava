import pandas as pd
from pathlib import Path

import utils.helper_functions as help_fn
import utils.convert as convert

class CreateActivities:
    def __init__(self) -> None:
        """ Get transform config data """
        self.cfg = help_fn.get_config()

        self.cfg_db = self.cfg.db.transform
        self.db_folder_path = Path(self.cfg_db.folder_path)
        self.activities_db_path = self.db_folder_path / self.cfg_db.activities_file_name

        self.df_columns = self.cfg.df.transform.activities.columns
        self.average_speed_column_name = self.cfg.df.transform.activities.average_speed_column_name

        self.body_parts_singular = self.cfg.df.transform.activities.body_parts.singular
        self.body_parts_plural = self.cfg.df.transform.activities.body_parts.plural
    
    def __refactor_time_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Add time informatino to df
        Args:
            df (pd.DataFrame): activities df
        Returns:
            df (pd.DataFrame): activities df with new time information
        """
        df.iloc[:,7] = pd.to_datetime(df.iloc[:, 7])
        df = df.sort_values(by=df.columns[7])
        df["month"] = df.iloc[:, 7].dt.to_period('M')
        df["year"] = df.iloc[:, 7].dt.to_period('Y')
        return df

    def __refactor_speed_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Add speed information to df
        Args:
            df (pd.DataFrame): activities df
        Returns:
            df (pd.DataFrame): activities df with new speed information
        """
        elapsed_time_hours_df = convert.seconds_to_hours(df.iloc[:,4])
        elevation_gain_km_df = convert.meters_to_kilometers(df.iloc[:,5])

        df.rename(columns={ df.columns[8]: self.average_speed_column_name}, inplace = True)
        df.iloc[:,8] = convert.mps_to_kph(df.iloc[:,8])

        df["speed"] = df.iloc[:,2] / elapsed_time_hours_df
        df["grade_adjusted_speed"] = (df["distance"] + elevation_gain_km_df) / \
                                    convert.seconds_to_hours(df["elapsed_time"])
        return df
    
    def __get_injury_score(self, note_list: list) -> int:
        """ Get the injury score of a note
        Args:
            note_list (list): e.g. "cuisse droite 2, mollets 3, cheville gauche 1"
        Returns:
            (int): injury score, e.g. 9 (= 2 + 3 * 2 + 1)
        """
        injury_score = 0
                
        for note_el in note_list:
            if help_fn.has_numbers(note_el):
                rating = help_fn.first_number(note_el)
                
                if help_fn.two_first_words(note_el) in self.body_parts_singular:
                    injury_score += rating
                elif help_fn.first_word(note_el) in self.body_parts_plural:
                    injury_score += rating * 2
        
        return injury_score
        
    def __add_injury_scores(self, df:pd.DataFrame) -> pd.DataFrame:
        """ Add a colum with an injury score, i.e. the sum of all the injury ratings
        Args:
            df (pd.DataFrame): activities df
        Returns:
            df (pd.DataFrame): activities df with injury score
        """
        injury_score_list = []

        for row in df.itertuples():
            note_str = row[11] # In current row, 11th col = col number 10

            if note_str:
                note_list = note_str.lower().split(',')
                injury_score = self.__get_injury_score(note_list)  
                injury_score_list.append(injury_score)
            else:
                injury_score_list.append(0)
        
        df['injury_score'] = injury_score_list
        return df

    def create_activities_db(self, extracted_df: pd.DataFrame) -> None:
        # Column indexes: 0. 'id', 1. 'name', 2. 'distance', 3. 'moving_time',
        # 4. 'elapsed_time', 5. 'total_elevation_gain', 6. 'type', 7. 'start_date',
        # 8. 'average_speed', 9. 'perceived_exertion', 10. 'private_note'
        df = extracted_df[self.df_columns]

        df["average_slope"] = df.iloc[:, 5] / (df.iloc[:, 2] / 2) # Column idx: 11,
        df["moving_%"] = df.iloc[:, 3] / df.iloc[:, 4] # Column idx: 12. 'moving_%'
        df["load"] = df.iloc[:, 3] * df.iloc[:, 9] # Column idx: 13. 'load'

        df.iloc[:, 2] = convert.meters_to_kilometers(df.iloc[:, 2])

        df = self.__refactor_time_data(df) # Column idx: 14. 'month', 15. 'year
        df = self.__refactor_speed_data(df) # Column idx: 16. 'speed', 17. 'grade_adjusted_speed'
        
        df.iloc[:, 10] = df.iloc[:, 10].fillna('')
        df = self.__add_injury_scores(df) # Column idx: 18. 'injury_score'
        
        df.to_pickle(self.activities_db_path)
        
