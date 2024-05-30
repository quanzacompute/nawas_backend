
from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with, reqparse

from app import db

import requests
from requests.status_codes import codes as STATUS

API_URL = "https://api.bgpview.io"
DEFAULT_UA = "Python-BGPView"
API_STATUS_OK = "ok"

###############
## APIClient ##
###############

# General API Error
class APIError(Exception):
    def __init__(self, message = "An API error occurred."):
        super(APIError, self).__init__(message)

# Specific Error based on response
class InvalidResponseError(APIError):
    def __init__(self, response = requests.Response, message = "Invalid response received from API."):
        super(InvalidResponseError, self).__init__("{} Code: {}, Body: {}".format(message, response.status_code, response.content))

# Specific Error based on the query
class QueryError(InvalidResponseError):
    def __init__(self, response = requests.Response, message = "Query error received from API."):
        super(QueryError, self).__init__(response, message)

# Class to manage api connection to BGPView
class BGPViewClient:
    def __init__(self, user_agent = None):
        if user_agent is None:
            user_agent = DEFAULT_UA
        self.s = requests.Session()
        self.s.headers["user-agent"] = user_agent

    def get(self, endpoint):
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        r = self.s.get("{}{}".format(API_URL, endpoint))
        if r.status_code == STATUS["ok"]:
            try:
                j = r.json()
                if j["status"] != API_STATUS_OK:
                    raise QueryError(r)
                return j
            except ValueError:
                pass  # handled below
        raise InvalidResponseError(r)

    def __del__(self):
        del self.s

    def get_asn_prefixes(self, asn):
        return self.get("/asn/{}/prefixes".format(asn))


    


