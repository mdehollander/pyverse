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
    """
    A class to access a specific dataset with ID `dataverse_id`
    """

    def __init__(self, id):
        self.id = id

    def get_url(self, endpoint, apikey=False):
        url = "https://{server}/api/datasets/{id}{endpoint}".format(server=config.server,
                                                                    id=self.id,
                                                                    endpoint=endpoint)
        if apikey:
            url += "?key={apikey}".format(apikey=config.api_token)

        print(url)
        return url

    def view_info(self):
        return requests.get(self.get_url("", apikey=True)).json()

    def view_files(self, version_id=None):
        if version_id is None:
            version_id = ":latest"
        return requests.get(self.get_url("/versions/{version}/files".format(version=version_id), apikey=True)).json()

    def get_datafiles(self):
        dfs = []
        for df in self.view_files()['data']:
            dfs.append(Datafile(df['datafile']['id'], df['datafile']['name']))
        return dfs


class Datafile(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def download(self):
        url = "https://{server}/api/access/datafile/{id}?format=original".format(server=config.server,
                                                                 id=self.id)
        with open(self.name, "wb") as f:
            f.write(requests.get(url).content)
