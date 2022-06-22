import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

import utils.helper_functions as help_fn

class PlotSummary:
    def __init__(self) -> None:
        """ Get plot config data """
        self.cfg = help_fn.get_config()

        self.cfg_db = self.cfg.db.plot
        self.db_folder_path = Path(self.cfg_db.folder_path)
        self.summary_db_path = self.db_folder_path / self.cfg_db.summary_file_name

    def plot_summary(self, pivot_table_df: pd.DataFrame) -> None:
        """ Save a pdf plot of Strava activities
        Args:
            pivot_table_df (pd.DataFrame): pivot table summary of activities
        """
        pivot_table_df = pivot_table_df[::-1]

        fig, axes = plt.subplots(nrows=2, ncols=2, constrained_layout=True)

        df0 = pivot_table_df[['sum_distance_run', 'sum_distance_ride']]
        df1 = pivot_table_df[['sum_elapsed_time_run', 'sum_elapsed_time_ride']] / 3600
        df2 = pivot_table_df[['sum_total_elevation_gain_run', 'sum_total_elevation_gain_ride']]
        df3 = pivot_table_df[['sum_load_run', 'sum_load_ride']]

        df0.plot(ax=axes[0,0], title='Distance (km)', kind='bar', figsize=(16,8), fontsize=6)
        df1.plot(ax=axes[0,1], title='Elapsed time (h)', kind='bar', stacked=True, fontsize=6)
        df2.plot(ax=axes[1,0], title='Elevation gain (m)', kind='bar', stacked=True, fontsize=6)
        df3.plot(ax=axes[1,1], title='Load', kind='bar', stacked=True, fontsize=6)

        for axes in [axes[0,0], axes[0,1], axes[1,0], axes[1,1]]:
            axes.yaxis.grid()

        plt.savefig(self.summary_db_path)
        