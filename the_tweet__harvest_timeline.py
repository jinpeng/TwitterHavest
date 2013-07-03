# -*- coding: utf-8 -*-

import sys
import json
from twitter__login import login
from twitter__util import makeTwitterRequest
from twitter__util import getNextQueryMaxIdParam


def usage():
    print 'Usage: $ %s <timeline name> [max_pages] [user]' % (sys.argv[0], )
    print
    print '\t<timeline name> in [home, user] and is required'
    print '\t0 < max_pages <= 16 for timeline_name in [home, user]'
    print 'Notes:'
    print '\t* ~800 statuses are available from the home timeline.'
    print '\t* ~3200 statuses are available from the user timeline.'
    print '\t* The public timeline must now be accessed with the streaming API.'
    print '\t* See https://dev.twitter.com/docs/api/1.1/get/statuses/sample for details'

    exit()


if len(sys.argv) < 2 or sys.argv[1] not in ('home', 'user'):
    usage()
if len(sys.argv) > 2 and not sys.argv[2].isdigit():
    usage()
if len(sys.argv) > 3 and sys.argv[1] != 'user':
    usage()

TIMELINE_NAME = sys.argv[1]
MAX_PAGES = int(sys.argv[2])

USER = None

KW = {  # For the Twitter API call
    'count': 200,
    'trim_user': 'true',
    'include_rts' : 'true',
    'since_id' : 1,
    }

if TIMELINE_NAME == 'user':
    USER = sys.argv[3]
    KW['screen_name'] = USER
if TIMELINE_NAME == 'home' and MAX_PAGES > 4:
    MAX_PAGES = 4
if TIMELINE_NAME == 'user' and MAX_PAGES > 16:
    MAX_PAGES = 16

t = login()

# Open file for storing json data
filename = 'tweets-%s-timeline' % (TIMELINE_NAME, )

if USER:
    filename = '%s-%s' % (filename, USER)

f = file(filename, 'wb')

api_call = getattr(t.statuses, TIMELINE_NAME + '_timeline')
tweets = makeTwitterRequest(api_call, **KW)
json.dump(tweets, f, indent=2)
print 'Fetched %i tweets' % len(tweets)

page_num = 1
while page_num < MAX_PAGES and len(tweets) > 0:

    # Necessary for traversing the timeline in Twitter's v1.1 API.
    # See https://dev.twitter.com/docs/working-with-timelines
    KW['max_id'] = getNextQueryMaxIdParam(tweets)

    api_call = getattr(t.statuses, TIMELINE_NAME + '_timeline')
    tweets = makeTwitterRequest(api_call, **KW)
    json.dump(tweets, f, indent=2)
    print 'Fetched %i tweets' % len(tweets)
    page_num += 1

f.close()
