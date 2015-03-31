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

    def get_objects(self):
        objects = []
        for obj in requests.get(self.get_url("/contents", apikey=True)).json()['data']:
            if obj['type'] == "dataverse":
                objects.append(Dataverse(obj['id']))
            elif obj['type'] == "dataset":
                objects.append(Dataset(obj['id']))
            else:
                print("skipping id={0}".format(obj['id']))
        return objects


class Dataset(object):

    def __init__(self, id):
        self.id = id

    def get_url(self, endpoint, apikey=False):
        url = "https://{server}/api/datasets/{id}{endpoint}".format(server=config.server,
                                                                    id=self.id,
                                                                    endpoint=endpoint)
        if apikey:
            url += "?key={apikey}".format(apikey=config.api_token)

        return url

    def view_info(self):
        return requests.get(self.get_url("", apikey=True)).json()

    def view_files(self):
        return requests.get(self.get_url("/files", apikey=True)).json()
