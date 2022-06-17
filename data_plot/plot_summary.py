import pandas as pd
import matplotlib.pyplot as plt

def main():
    pivot_table_df = pd.read_pickle('./db/pivot_table.pkl')
    pivot_table_df[::-1]

    fig, axes = plt.subplots(nrows=2, ncols=2, constrained_layout=True)

    df0 = pivot_table_df[['sum_distance_run', 'sum_distance_ride']]
    df1 = pivot_table_df[['sum_elapsed_time_run', 'sum_elapsed_time_ride']] / 3600
    df2 = pivot_table_df[['sum_elevation_gain_run', 'sum_elevation_gain_ride']]
    df3 = pivot_table_df[['sum_load_run', 'sum_load_ride']]

    df0.plot(ax=axes[0,0], title='Distance (km)', kind='bar', figsize=(16,8), fontsize=6)
    df1.plot(ax=axes[0,1], title='Elapsed time (h)', kind='bar', stacked=True, fontsize=6)
    df2.plot(ax=axes[1,0], title='Elevation gain (m)', kind='bar', stacked=True, fontsize=6)
    df3.plot(ax=axes[1,1], title='Load', kind='bar', stacked=True, fontsize=6)

    for axes in [axes[0,0], axes[0,1], axes[1,0], axes[1,1]]:
        # axes.xaxis.set_major_locator(ticker.MaxNLocator(12))
        axes.yaxis.grid()

    plt.savefig('./plot/pivot_table_plot.pdf')

if __name__ == '__main__':
    main()
