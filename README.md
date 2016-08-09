# ScopusScrapus - A small utility for the Scopus Search API
Elsevier is kind enough to make its database of scientific papers accessible through a web API. This
small Python module allows you to access it programatically with Python.

Documentation for the Scopus Search API is available here: http://api.elsevier.com/documentation/SCOPUSSearchAPI.wadl
Documentation on how to construct then search queries is here: http://api.elsevier.com/documentation/search/SCOPUSSearchTips.htm

## Installation

The little ScopusScrapus package is available on PyPi, and it can be easily installed:

```
pip3 install ScopusScrapus
```

## Usage
To use the Scopus Search API (and all other APIs provided by Elsevier) require an API key to use. To get one you
should visit their Devlopers site here: http://dev.elsevier.com/index.html.

To run a scopus search query looking for papers mentioning 'arctic' in their title, abstract or keywords and that were
published between 2008 and 2009, you do the following:

```
from ScopusScrapus import ScopusSearchQuery

params = {'query':'TITLE-ABS-KEY(arctic)', 'date':'2008-2009'}
ssq = ScopusSearchQuery(key,params)
# Key is your API key, and params is a dictionary
# containing your query and other fields.
# optionally, a timeout parameter can be passed to the constructor. It should contain a number of seconds after which the query will be aborted if no response has been received from the scopus api. In this case, an exception requests.exceptions.ReadTimeout will be raised
# The default parameters are:

defaultParams = {'count':100,
    'view':'COMPLETE'}

# The complete view can only be seen by entities
# subscribing to scopus so make sure to override it
# in your params dictionary if you are not.
```

Once the `ScopusSearchQuery` object has been created you can iterate through it as a normal iterator:

```
for paper in ssq:
    print(str(paper))
```

Each result has the normal Scopus Search API format.
