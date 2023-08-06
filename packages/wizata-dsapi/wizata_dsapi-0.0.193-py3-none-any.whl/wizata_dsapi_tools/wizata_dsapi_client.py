import requests
from wizatads.wizata_dsapi import request

class WizataDSAPIClient:

    def __init__(self):
        self.domain = None
        self.user = None
        self.password = None

    def __url(self):
        return "https://" + self.user + ":" + self.password + "@" + self.domain + "/dsapi/"

    def __header(self):
        return {'Content-Type': 'application/json'}

    def __request_process(self, method, route):
        response = requests.request(method, self.__url() + route, headers=self.__header())
        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError(str(response.status_code) + " - " + response.reason)

    def get_infos(self):
        return self.__request_process("GET", "get_infos")

    def get_ds_functions(self):
        return self.__request_process("GET", "get_ds_functions")

    def get_datas(self, query: request):
        return query.prepare()
