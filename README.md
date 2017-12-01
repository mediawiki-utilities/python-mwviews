# Wikimedia Foundation Pageview Tools

This project is a collection of tools used to parse and query Wikimedia Foundation pageview data, from both static dumps and the online API.

## Install

`pip install mwviews`

## pageview API

```
from mwviews.api import PageviewsClient

p = PageviewsClient()

p.article_views('en.wikipedia', ['Selfie', 'Cat', 'Dog'])
p.project_views(['ro.wikipedia', 'de.wikipedia', 'commons.wikimedia'])
p.top_articles('en.wikipedia', limit=10)
p.article_views('en.wikipedia', ['Selfie', 'Cat'], granularity='monthly', start='20160201', end='20160331')

# Feel free to add your own features in pull requests!
```

When querying for multiple articles and multiple projects the client uses `ThreadPoolExecutor` to parallelize.  You can set the level of parallelism when you instantiate the client like `p = PageviewsClient(10)`.
