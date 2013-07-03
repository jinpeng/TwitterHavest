# -*- coding: utf-8 -*-

import sys
import json
from twitter__login import login

Q = sys.argv[1]
MAX_PAGES = 5

filename = 'search-%s' % (Q.lower().replace('#', '').replace('@', ''), )

t = login()
search_results = t.search.tweets(q=Q, count=100)
tweets = search_results['statuses']

for _ in range(MAX_PAGES-1): # Get more pages
    next_results = search_results['search_metadata']['next_results']

    # Create a dictionary from the query string params
    kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ]) 

    search_results = t.search.tweets(**kwargs)
    tweets += search_results['statuses']

    if len(search_results['statuses']) == 0:
        break

    print 'Fetched %i tweets so far' % (len(tweets),)

# Store the data
f = file('out/' + filename, 'wb')
json.dump(tweets, f, indent=2)
f.close()
print 'Done. Stored data to file out/%s' % (filename,)
