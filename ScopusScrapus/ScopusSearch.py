import requests as r
import urllib.parse as purl
import json

def StartScopusSearch(key,params):
    ssq = ScopusSearchQuery(key,params)
    return ssq

class ScopusSearchQuery:
    _defaultParams = {'count':100,
                      'view':'COMPLETE',
                      'httpAccept':'application/json'}
    _baseUrl = "http://api.elsevier.com/content/search/scopus?"

    def __init__(self,key,params):
        self._apiKey = key
        self._keys = None
        if type(key) == type([]):
            self._keys = key
            self._keyCount = 0
            self._apiKey = key[0]
        self._state = "empty"
        self._params = params
        self._data = []
        self._nextUrl = None
        self._i = 0
        self._count = 0

    def _make_search_url(self):
        params = self._params
        defParams = ScopusSearchQuery._defaultParams
        pSet = set(params.keys()).union(set(defParams.keys()))
        parameters = {key:params[key] if key in params else defParams[key] for key in pSet}

        querystring = purl.urlencode(parameters)
        apiKeyString = purl.urlencode({'apiKey':self._apiKey})
        url = "{}{}{}{}".format(ScopusSearchQuery._baseUrl,querystring,'&',apiKeyString)
        return url

    def _manageQuotaExcess(self,raiseOnQE = False):
        print("Managing quota exess...")
        if raiseOnQE or self._keys is None:
            raise Exception("QuotaExceeded - You must wait 7 days until quotas are reset")
        self._nextUrl = None
        self._keyCount = (self._keyCount + 1) % len(self._keys)
        print("Key was: "+self._apiKey)
        self._apiKey = self._keys[self._keyCount]
        print("Key is: "+self._apiKey)
        return self._run_search(True) # If we fail again, we surrender

    def _run_search(self, raiseOnQE = False):
        url = self._nextUrl
        if url is None: url = self._make_search_url()
        if url == "done": raise StopIteration()

        qRes = r.get(url)
        dta = qRes.json()
        if qRes.status_code == 429:
            return self._manageQuotaExcess(raiseOnQE)
        if qRes.status_code != 200:
            raise Exception("{} {} {} {}".format("Error: ",
                                                 dta['service-error']['status']['statusText'],
                                                 "URL is:",url)) # Fix this

        # KeyError hazard: If no 'next' url is available, we need to error out anyway
        nxtLink = [ln for ln in dta['search-results']['link'] if ln['@ref'] == 'next']
        if len(nxtLink) > 0: self._nextUrl = nxtLink[0]['@href']
        else: self._nextUrl = "done" # Nasty? Sorry : )
        return dta['search-results']['entry'] # Returning only the obtained results
    
    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if self._i == len(self._data):
            self._data = self._run_search()
            self._i = 0
        if len(self._data) == self._i:
            pass # Raise error
        self._i += 1
        return self._data[self._i-1]











