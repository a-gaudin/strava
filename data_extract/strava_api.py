import requests
import urllib3

from utils.helper_functions import get_config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class StravaAPI:
    def __init__(self) -> None:
        """ Init request data """
        self.cfg = get_config().strava_request
        self.auth_url = self.cfg.auth_url
        self.activities_url = self.cfg.activities_url
        self.access_request_params = self.cfg.request_params.access
        self.activity_request_params = self.cfg.request_params.activity
        self.request_batch_size = self.cfg.request_limits.batch_size
        self.headers = self.__get_headers()
    
    def __get_headers(self) -> dict:
        """ Get request header for Strava request
        Returns:
            (dict): request header
        """
        res = requests.post(self.auth_url, data=self.access_request_params, verify=False)
        access_token = res.json()['access_token']
        return {'Authorization': f'Bearer {access_token}'}

    def get_activity(self, id:int) -> str:
        """ Get one Strava activity's data
        Args:
            id (int): Strava activity id
        Returns:
            (str): json of the activity data
        """
        activity_url = self.activities_url + '/' +  str(id) # should be a string as Strava API can't handle a Pathlib Path
        params = self.activity_request_params
        activity_json = requests.get(activity_url, headers=self.headers, params=params).json()
        print(f'Strava API response message: {activity_json}')
        return activity_json

    def get_all_activities(self) -> str:
        """ Get all Strava activities data
        Returns:
            (str): json of all activities data
        """
        activities_left_to_get = True
        page = 1
        activities_json = []

        while activities_left_to_get == True:
            params = {
                'per_page': self.request_batch_size,
                'page': page
            }
            new_activities_json = requests.get(self.activities_url,
                headers=self.headers, params=params).json()
            print(f'Strava API response message: {new_activities_json}')
            activities_json += new_activities_json
            page += 1

            if len(new_activities_json) < self.request_batch_size:
                activities_left_to_get = False
        return activities_json
