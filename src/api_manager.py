import requests

class ApiRequestManager:
    @staticmethod
    def get(url):
        return requests.get(url)
