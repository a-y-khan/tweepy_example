import configparser

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

import re


class MyStreamListener(StreamListener):
    def strip_emojis(self, tweet_text: str):
        # TODO: this is only the first match in the emoji unicode table
        emoji_list1 = re.compile(u'[\U0001f300-\U0001f5fF]')
        stripped_tweet_text = emoji_list1.sub(' ', tweet_text)

        return stripped_tweet_text

    def on_status(self, status):
        tweet = self.strip_emojis(status.text)
        print('tweet: [{}]'.format(tweet))

        # TODO: accumulate?

    def on_error(self, status_code):
        if status_code == 420:
            print("rate limited!")
            return False


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    default_config = config['DEFAULT']

    auth = OAuthHandler(default_config.get('CONSUMER_KEY'), default_config.get('CONSUMER_SECRET'))
    auth.set_access_token(default_config.get('ACCESS_KEY'), default_config.get('ACCESS_SECRET'))
    api = API(auth)

    my_stream_listener = MyStreamListener()
    my_stream = Stream(auth=api.auth, listener=my_stream_listener)

    # basic - works!
    # my_stream.sample(languages=['en'])

    # filter - works!
    my_stream.filter(track=['facebook'], languages=['en'])

