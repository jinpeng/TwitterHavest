# -*- coding: utf-8 -*-

import os
import twitter
import ConfigParser

from twitter.oauth import write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance


def login():

    config = ConfigParser.ConfigParser()
    config.readfp(open("twitter.config","rb"))

    # Go to http://twitter.com/apps/new to create an app and get these items
    # See also http://dev.twitter.com/pages/oauth_single_token

    APP_NAME = config.get('account', 'appname')
    CONSUMER_KEY = config.get('account', 'consumerkey')
    CONSUMER_SECRET = config.get('account', 'consumersecret')
    ACCESS_TOKEN = config.get('account', 'accesstoken')
    ACCESS_TOKEN_SECRET = config.get('account', 'accesstokensecret')
    TOKEN_FILE = 'out/twitter.oauth'

    try:
        (oauth_token, oauth_token_secret) = read_token_file(TOKEN_FILE)
    except IOError, e:
        if ACCESS_TOKEN != None and ACCESS_TOKEN_SECRET != None:
            oauth_token = ACCESS_TOKEN
            oauth_token_secret = ACCESS_TOKEN_SECRET
        else:
            (oauth_token, oauth_token_secret) = oauth_dance(APP_NAME, CONSUMER_KEY,
                CONSUMER_SECRET)

        if not os.path.isdir('out'):
            os.mkdir('out')

        write_token_file(TOKEN_FILE, oauth_token, oauth_token_secret)
         
    return twitter.Twitter(domain='api.twitter.com', api_version='1.1',
                        auth=twitter.oauth.OAuth(oauth_token, oauth_token_secret,
                        CONSUMER_KEY, CONSUMER_SECRET))

if __name__ == '__main__':
    login()
