import pandas as pd

def get_summary(df):
    """ Returns a pivot table dataframe that summarizes the activities """
    df = df[df["type"].isin(["Run", "Ride"])]
    pivot_table = pd.pivot_table(df, values=['distance', 'elapsed_time', 'elevation_gain'],
                                index=['month'], columns=['type'], aggfunc=["sum"], fill_value=0)
    pivot_table = pivot_table.sort_values(by=["month"], ascending=False)
    # pivot_table = pd.to_datetime(pivot_table["sum"]["elapsed_time"]["Run"], unit='s').dt.time
    return pivot_table

# def main():
    # summary_df = get_summary(activities_df)
    # print(summary_df.head(10)) 

# if __name__ == "__main__":
#     main()