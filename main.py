from utils.helper_functions import get_config, get_df_from_db

from data_extract.extract import ExtractStravaData
from data_transform.activities import CreateActivities
from data_transform.injuries import CreateInjuries
from data_transform.summary import SummarizeActivities
from data_plot.plot_summary import PlotSummary
from data_plot.plot_injury_factors import PlotInjuryFactors

def main() -> None:
    ExtractStravaData().update_strava_activities_db()

    cfg = get_config()
    strava_activities_df = get_df_from_db(cfg.db.extract.folder_path, cfg.db.extract.activities_file_name)
    CreateActivities().create_activities_db(strava_activities_df)

    activities_df = get_df_from_db(cfg.db.transform.folder_path, cfg.db.transform.activities_file_name)
    CreateInjuries().create_injuries_db(activities_df)

    PlotInjuryFactors().plot_injury_factors(activities_df)
    SummarizeActivities().create_summary_db(activities_df)

    summary_df = get_df_from_db(cfg.db.transform.folder_path, cfg.db.transform.summary_file_name)
    PlotSummary().plot_summary(summary_df)

if __name__ == "__main__":
    main()