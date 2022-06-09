import pandas as pd

def get_pivot_table(df):
    """ Returns a pivot table dataframe that summarizes the activities """
    df = df[df['type'].isin(['Run', 'Ride'])]
    df = pd.pivot_table(df, values=['distance', 'elapsed_time', 'elevation_gain'],
                        index=['month'], columns=['type'], aggfunc=['sum'], fill_value=0)
    df = df.sort_values(by=['month'], ascending=False)
    return df

def flatten(df):
    """ Converts multi-index dataframe to a single-level columns"""
    df.columns = [('_'.join(col).strip()).lower() for col in df.columns.values]
    return df

def main():
    activities_df = pd.read_pickle('./db/activities_load.pkl')
    pivot_table_df = get_pivot_table(activities_df)
    pivot_table_df = flatten(pivot_table_df)

    pivot_table_df.to_pickle('./db/pivot_table.pkl')

    pd.set_option('display.max_columns', None)
    print(pivot_table_df.head(10))

if __name__ == '__main__':
    main()