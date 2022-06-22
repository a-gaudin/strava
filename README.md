# Strava logs insight
Visualize trainings logs from a [Strava](https://www.strava.com/) account and analyse factors causing soreness and injuries.

* Language: Python
* Libraries: Pandas, Maplotlib, Scikit-learn

## Setup
1. [Activate the Strava API](https://developers.strava.com/docs/getting-started/) for your account with ```read-all``` access
2. Modify ```conf/config.yaml``` with your personal API client data
3. Run ```main.py``` (extracts all your Strava activities)
4. Analyse resulting pdf plots in ```data_plot/plots```

## Conclusions from my own Strava data
- To avoid soreness/injuries: Do not run with recent injuries, keep intensity low
- Contrary to popular belief, my training load have a minimal impact on injuries (at least for the levels of load that I reach)
