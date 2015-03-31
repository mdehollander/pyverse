import requests

class Connection(object):

    def __init__(self, api_token=None, server=None):
        self.api_token = api_token
        self.server = server

    @property
    def root(self):
        return Dataverse(':root', api_token=self.api_token, server=self.server)


class BaseDataverseObject(object):

    def __init__(self, id=None, api_token=None, server=None):
        self.id = id
        self.api_token = api_token
        self.server=server
        

class Dataverse(BaseDataverseObject):
    """
    A class to access a specific dataverse with ID `dataverse_id`
    """

    def get_url(self, endpoint, apikey=False):
        url = "https://{server}/api/dataverses/{id}{endpoint}".format(server=self.server,
                                                                     id=self.id,
                                                                     endpoint=endpoint)
        if apikey:
            url += "?key={apikey}".format(apikey=self.api_token)

        return url

    def view_info(self):
        return requests.get(self.get_url("", apikey=True)).json()

    @property
    def dataverses(self):
        objects = []
        for obj in requests.get(self.get_url("/contents", apikey=True)).json()['data']:
            if obj['type'] == "dataverse":
                objects.append(Dataverse(obj['id'], api_token=self.api_token, server=self.server))
        return objects
        
    @property
    def datasets(self):
        objects = []
        for obj in requests.get(self.get_url("/contents", apikey=True)).json()['data']:
            if obj['type'] == "dataset":
                objects.append(Dataset(obj['id'], api_token=self.api_token, server=self.server))
        return objects


class Dataset(BaseDataverseObject):
    """
    A class to access a specific dataset with ID `dataverse_id`
    """

    def get_url(self, endpoint, apikey=False):
        url = "https://{server}/api/datasets/{id}{endpoint}".format(server=self.server,
                                                                    id=self.id,
                                                                    endpoint=endpoint)
        if apikey:
            url += "?key={apikey}".format(apikey=self.api_token)

        return url

    def view_info(self):
        return requests.get(self.get_url("", apikey=True)).json()

    def view_files(self, version_id=None):
        if version_id is None:
            version_id = ":latest"
        return requests.get(self.get_url("/versions/{version}/files".format(version=version_id), apikey=True)).json()

    @property
    def datafiles(self):
        dfs = []
        for df in self.view_files()['data']:
            dfs.append(Datafile(df['datafile']['name'], id=df['datafile']['id'], api_token=self.api_token, server=self.server))
        return dfs


class Datafile(BaseDataverseObject):

    def __init__(self, name, **kwargs):
        self.name = name
        super(Datafile, self).__init__(**kwargs)

    def download(self):
        url = "https://{server}/api/access/datafile/{id}?format=original".format(server=self.server,
                                                                 id=self.id)
        with open(self.name, "wb") as f:
            f.write(requests.get(url).content)
