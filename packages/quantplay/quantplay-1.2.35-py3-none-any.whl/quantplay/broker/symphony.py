import traceback
import requests
import json

from quantplay.broker.generics.broker import Broker
from quantplay.utils.constant import Constants, timeit


class Symphony(Broker):
    source = "WebAPI"

    symphony_secret_key = "symphony_secret_key"
    symphony_app_key = "symphony_app_secret"

    base_url = "https://developers.symphonyfintech.in"

    headers = {
        "Content-Type": "application/json",
    }

    @timeit(MetricName="Symphony:__init__")
    def __init__(self, headers=None, api_secret=None, api_key=None):
        super(Symphony, self).__init__()

        if headers:
            self.headers = headers

        try:
            if headers:
                self.profile()
            else:
                self.generate_token(api_secret, api_key)
                self.account_summary()

        except Exception as e:
            print(traceback.print_exc())
            raise e

    def generate_token(self, api_secret, api_key):
        data = {
            "secretKey": api_secret,
            "appKey": api_key,
            "source": self.source,
        }

        session_login_url = f"{self.base_url}/interactive/user/session"

        response = requests.post(
            session_login_url, headers=self.headers, data=json.dumps(data)
        )
        resp_json = response.json()

        Constants.logger.info(f"login response {resp_json}")

        self.headers["authorization"] = resp_json["result"]["token"]
        self.ClientID = resp_json["result"]["clientCodes"][0]

    def account_summary(self):

        get_profile_url = f"{self.base_url}/interactive/user/balance"

        response = requests.get(
            get_profile_url,
            headers=self.headers,
            params={"clientID": self.ClientID},
        ).json()

        if response["type"] == "error":
            raise Exception(response["description"])

        api_response = response["result"]["BalanceList"][0]["limitObject"]
        response = {
            # TODO: Get PNL
            "pnl": 0,
            "margin_used": api_response["RMSSubLimits"]["marginUtilized"],
            "margin_available": api_response["RMSSubLimits"]["netMarginAvailable"],
        }

        return response

    def profile(self):

        get_profile_url = f"{self.base_url}/interactive/user/profile"

        api_response = requests.get(
            get_profile_url,
            params={"clientID": self.ClientID},
            headers=self.headers,
        ).json()

        if api_response["type"] == "error":
            raise Exception(api_response["description"])

        api_response = api_response["result"]
        response = {
            "user_id": api_response["ClientId"],
            "full_name": api_response["ClientName"],
            "segments": api_response["ClientExchangeDetailsList"],
        }

        return response
