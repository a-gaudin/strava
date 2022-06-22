import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import mutual_info_classif
from pathlib import Path

import utils.helper_functions as help_fn

class PlotInjuryFactors:
    def __init__(self) -> None:
        """ Get plot config data """
        self.cfg = help_fn.get_config()

        self.cfg_db = self.cfg.db.plot
        self.db_folder_path = Path(self.cfg_db.folder_path)
        self.correlations_file_path = self.db_folder_path / self.cfg_db.correlations_file_name
        self.factors_file_path = self.db_folder_path / self.cfg_db.factors_file_name

        self.cfg_injuries = self.cfg.df.plot.injuries
        self.notes_start_date = self.cfg_injuries.notes_start_date
        self.sports = self.cfg_injuries.sports
        self.selected_features = self.cfg_injuries.selected_features
        self.target_feature = self.cfg_injuries.target_feature
        self.plot_title = self.cfg_injuries.plot_title
    
    def __plot_correlations(self, df: pd.DataFrame) -> None:
        """ Save a pdf plot of correlations between features
        Args:
            df (pd.DataFrame): activities data
        """
        df = df[::-1]  # reverse temporality
        corr_df = df.corr()
        plt.figure(figsize=(11,6))
        sns.heatmap(corr_df, annot=True)
        plt.subplots_adjust(left=0.2, bottom=0.35)
        plt.savefig(self.correlations_file_path)
        plt.close()

    def __plot_feature_importances(self, df: pd.DataFrame) -> None:
        """ Save a pdf plot of feature importances on injuries
        Args:
            df (pd.DataFrame): activities data
        """
        X_df = df[self.selected_features]
        y_df = df[self.target_feature]
        
        feature_importances = mutual_info_classif(X_df, y_df, random_state=0, n_neighbors=3, discrete_features='auto')
        feature_importances = pd.Series(feature_importances, X_df.columns)
        feature_importances.plot(kind='barh', title=self.plot_title)
        plt.subplots_adjust(left=0.3)
        plt.savefig(self.factors_file_path)
        plt.close()

    def plot_injury_factors(self, activities_df: pd.DataFrame) -> None:
        activities_df = activities_df[(activities_df.iloc[:, 7] > self.notes_start_date)] # filter out older activities without injury notes
        activities_df = activities_df[activities_df.iloc[:, 6].isin(self.sports)]

        print(activities_df.shape)

        self.__plot_correlations(activities_df)    
        self.__plot_feature_importances(activities_df)
        