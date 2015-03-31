import requests

class Conf(object):
    api_token = None
    server = None

config = Conf()


class Dataverse(object):
    """
    A class to access a specific dataverse with ID `dataverse_id`
    """

    def __init__(self, id):
        self.id = id

    def get_url(self, endpoint, apikey=False):
        url = "https://{server}/api/dataverses/{id}{endpoint}".format(server=config.server,
                                                                     id=self.id,
                                                                     endpoint=endpoint)
        if apikey:
            url += "?key={apikey}".format(apikey=config.api_token)

        return url

    def view_info(self):
        return requests.get(self.get_url("", apikey=True)).json()
