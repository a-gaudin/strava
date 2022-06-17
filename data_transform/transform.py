import pandas as pd
from pathlib import Path

from utils.helper_functions import get_config
import utils.convert as convert

class Transform:
    def __init__(self) -> None:
        """ Get transform config data """
        self.cfg = get_config()

        self.cfg_db = self.cfg.db.transform
        self.db_folder_path = Path(self.cfg_db.folder_path)
        self.activities_db_path = self.db_folder_path / self.cfg_db.activities_file_name

        self.df_columns = self.cfg.activities_df_columns
        self.average_speed_col_new_name = self.cfg.average_speed_col_new_name

        self.body_parts_singular = self.cfg.body_parts_singular
        self.body_parts_plural = self.cfg.body_parts_plural

    def __refactor_speed_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Add speed informatino to df
        Args:
            df (pd.DataFrame): activities df
        Returns:
            df (pd.DataFrame): activities df with new speed information
        """
        elapsed_time_hours_df = convert.seconds_to_hours(df.iloc[:,4])
        elevation_gain_km_df = convert.meters_to_kilometers(df.iloc[:,5])

        df.rename(columns={ df.columns[8]: self.average_speed_col_new_name}, inplace = True)
        df.iloc[:,8] = convert.mps_to_kph(df.iloc[:,8])

        df["speed"] = df.iloc[:,2] / elapsed_time_hours_df
        df["grade_adjusted_speed"] = (df["distance"] + elevation_gain_km_df) / \
                                    convert.seconds_to_hours(df["elapsed_time"])
        return df
    
    def __add_injury_score(self, df:pd.DataFrame) -> pd.DataFrame:
        """ Add a colum with an injury score, i.e. the sum of all the injury ratings
        Args:
            df (pd.DataFrame): activities df
        Returns:
            df (pd.DataFrame): activities df with injury score
        """
        injury_score_list = []

        for row in df.itertuples():
            note_str = row[:,10]
            note_list = note_str.lower().split(',')
            injury_score = 0
            
            for note_el in note_list:
                if note_el in self.body_parts_singular:
                    injury_score += 1
                
                if note_el in self.body_parts_plural:
                    injury_score += 2
            
            injury_score_list.append(injury_score)
        
        df['injury_score'] = injury_score_list
        return df

    def create_activities_db(self, df: pd.DataFrame) -> None:
        # Column indexes: 0. 'id', 1. 'name', 2. 'distance', 3. 'moving_time',
        # 4. 'elapsed_time', 5. 'total_elevation_gain', 6. 'type', 7. 'start_date',
        # 8. 'average_speed', 9. 'perceived_exertion', 10. 'private_note'
        activities_df = df[self.df_columns]

        df["average_slope"] = df.iloc[:,5] / (df.iloc[:,2] / 2) # Column idx: 11
        df["moving_%"] = df.iloc[:,3] / df.iloc[:,4] # Column idx: 12
        df["load"] = df.iloc[:,3] * df.iloc[:,9] # Column idx: 13
        df["month"] = df.iloc[:,7].dt.to_period('M') # Column idx: 14
        df["year"] = df.iloc[:,7].dt.to_period('Y') # Column idx: 15

        df.iloc[:,2] = convert.meters_to_kilometers(df.iloc[:,2])
        df.iloc[:,7] = pd.to_datetime(df.iloc[:,7])

        activities_df = self.__refactor_speed_data(activities_df) # Column idx: 16. 'speed', 17. 'grade_adjusted_speed'
        activities_df = self.__add_injury_score(activities_df) # Column idx: 18. 'injury_score'
        
        activities_df.to_pickle(self.activities_db_path)
