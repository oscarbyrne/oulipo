import abc
from os.path import join

import requests

from .keys import mashape_key


class RestAPI(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def headers(self):
        return {}

    @abc.abstractproperty
    def base_url(self):
        return ""

    def get(self, method, **kwargs):
        request = join(self.base_url, method)
        return requests.get(request, headers=self.headers, **kwargs).json()



class MashapeAPI(RestAPI):

    headers = {
        "X-Mashape-Key": mashape_key,
        "Accept": "application/json",
    }

    @abc.abstractproperty
    def name(self):
        return ""

    @property
    def base_url(self):
        return "https://{}.p.mashape.com/".format(self.name)


