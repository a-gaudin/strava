# Strava logs insights
Visualize trainings logs from a Strava account (https://www.strava.com/)

* Languages: Python
* Library: Pandas

## Instructions:
1. Fill in API request parameters in a config.py file, 
```
token_request_params = {
    'client_id': "CLIENT_ID_TBD",
    'client_secret': 'CLIENT_SECRET_TBD',
    'refresh_token': 'REFRESH_TOKEN_TBD',
    'grant_type': "refresh_token",
    'f': 'json'
}

activities_request_params = {
    'per_page': 200,
    'page': 1
}
```
2. Run main.py