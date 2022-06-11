import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import mutual_info_classif

def correlation_plot(df):
    corr = df.corr()
    plt.figure(figsize=(10,6))
    sns.heatmap(corr, annot=True)
    plt.subplots_adjust(left=0.2, bottom=0.35)
    plt.savefig('./plot/injury_correlations.pdf')

def feature_importance(df):
    X_df = df.drop(['sum_injury_score'], axis=1)
    print(f'X: {X_df.shape}')
    y_df = df['sum_injury_score']
    print(f'y: {y_df.shape}')
    threshold = 3
    
    # high_score_features1 = []
    # feature_scores = mutual_info_classif(X_df, y_df, random_state=0, n_neighbors=3,discrete_features='auto')
    # for score, f_name in sorted(zip(feature_scores, X_df.columns), reverse=True)[:threshold]:
    #         print(f_name, score)
    #         high_score_features1.append(f_name)

def main():
    pivot_table_df = pd.read_pickle('./db/injury_pivot_table.pkl')
    pivot_table_df = pivot_table_df[::-1] # reverse temporality

    correlation_plot(pivot_table_df)
    feature_importance(pivot_table_df)

if __name__ == '__main__':
    main()
