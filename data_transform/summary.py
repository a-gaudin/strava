import pandas as pd
from pathlib import Path

import utils.helper_functions as help_fn
import utils.convert as convert

class SummarizeActivities:
    def __init__(self) -> None:
        """ Get transform config data """
        self.cfg = help_fn.get_config()

        self.cfg_db = self.cfg.db.transform
        self.db_folder_path = Path(self.cfg_db.folder_path)
        self.summary_db_path = self.db_folder_path / self.cfg_db.summary_file_name

        self.summary_sports = self.cfg.summary.sports
        self.summary_metrics = self.cfg.summary.metrics
        self.summary_column = self.cfg.summary.column
        self.summary_row = self.cfg.summary.row
    
    def __get_pivot_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Get a pivot table that summarizes the activities with load data
        Args:
            df (pd.DataFrame): all activities data
        Returns:
            df (pd.DataFrame): pivot table summary of activities with load data
        """
        df = df[df[self.summary_column].isin(self.summary_sports)]
        df = df.dropna()
        # df = pd.pivot_table(df, values=['distance', 'elapsed_time', 'total_elevation_gain', 'load'],
        #                 index=['month'], columns=['type'], aggfunc=['sum'], fill_value=0)
        df = pd.pivot_table(df, values=self.summary_metrics, index=['month'],
                            columns=['type'], aggfunc=['sum'], fill_value=0)
        df = df.sort_values(by=[self.summary_row], ascending=False)
        return df

    def __flatten(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Convert multi-index dataframe to a single-level columns
        Args:
            df (pd.DataFrame): activities's pivot table with multi-level columns
        Returns:
            df (pd.DataFrame): activities's pivot table with single-level columns
        """
        df.columns = [('_'.join(col).strip()).lower() for col in df.columns.values]
        return df

    def __add_grand_total(self, df:pd.DataFrame) -> pd.DataFrame:
        """ Add grand totals to the pivot table summary
        Args:
            df (pd.DataFrame): activities's pivot table without grand total
        Returns:
            df (pd.DataFrame): activities's pivot table with grand total
        """
        print("hello")
        df['sum_elapsed_time'] = df['sum_elapsed_time_run'] + df['sum_elapsed_time_ride']
        df['sum_elevation_gain'] = df['sum_elevation_gain_run'] + df['sum_elevation_gain_ride']
        df['sum_load'] = df['sum_load_run'] + df['sum_load_ride']
        return df

    def create_summary_db(self, df: pd.DataFrame) -> None:
        pivot_table_df = self.__get_pivot_table(df)
        pivot_table_df = self.__flatten(pivot_table_df)
        print(pivot_table_df.head(5))
        pivot_table_df = self.__add_grand_total(pivot_table_df)

        pivot_table_df.to_pickle(self.summary_db_path)
        