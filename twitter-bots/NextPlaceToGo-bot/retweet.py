import tweepy
import logging
from config import create_api
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class RetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        tweepy.StreamListener.__init__(self)
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")

        # If a tweet is a reply or I'm its author, ignore it
        if tweet.in_reply_to_status_id is not None or \
           tweet.user.id == self.me.id:
            return

        # If the tweet has never been tweeted, the retweet it
        if not tweet.retweeted:
            try:
                tweet.retweet()

            # TODO: find out what this is for
            except Exception as e:
                logger.error("Error on retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)


def main(keywords):
    api = create_api()
    tweets_listener = RetweetListener(api)

    # Create a stream object
    stream = tweepy.Stream(api.auth, tweets_listener)

    # Filter tweets that match the keywords argument
    stream.filter(track=keywords, languages=["en"])


if __name__ == '__main__':
    main(["#travel"])