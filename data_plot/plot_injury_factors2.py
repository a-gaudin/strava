import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import mutual_info_classif

def correlation_plot(df):
    df = df[::-1]  # reverse temporality
    corr_df = df.corr()
    plt.figure(figsize=(10,6))
    sns.heatmap(corr_df, annot=True)
    plt.subplots_adjust(left=0.2, bottom=0.35)
    plt.savefig('./plot/injury_correlations.pdf')

def feature_importances_plot(df):
    df = df[df['type'].isin(['Run'])]
    df = df.dropna()

    X_df = df[['distance', 'moving_time', 'elevation_gain' , 'moving_speed', 'grade_adjusted_speed', 'moving_%', 'perceived_exertion', 'load']]
    y_df = df['injury_score']
    
    feature_importances = mutual_info_classif(X_df, y_df, random_state=0, n_neighbors=3, discrete_features='auto')
    feature_importances = pd.Series(feature_importances, X_df.columns)
    feature_importances.plot(kind='barh', title='Factors causing injuries/soreness while running')
    plt.subplots_adjust(left=0.3)
    plt.savefig('./plot/injury_factors.pdf')

def main():
    pivot_table_df = pd.read_pickle('./db/injury_pivot_table.pkl')
    correlation_plot(pivot_table_df)
    
    injury_df = pd.read_pickle('./db/injury.pkl')
    feature_importances_plot(injury_df)

if __name__ == '__main__':
    main()
