import tweepy
import logging
import os

logger = logging.getLogger()


def create_api():
    # consumer_key = os.getenv("CONSUMER_KEY")
    # consumer_secret = os.getenv("CONSUMER_SECRET")
    # access_token = os.getenv("ACCESS_TOKEN")
    # access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    consumer_key = "7oZ7h3u7PEivhJxDOp42xHi2J"
    consumer_secret = "1pM4KELZEpyzfUdEkkUOkXyYphCuEeI04BSPtsQhnxpCeQQMPd"
    access_token = "1266741712845631489-DuqoM8Kkv9oEy4TtR4TVFsVO8zpDr8"
    access_token_secret = "uDPRS1hV7gxtp6ZVbC3mwSQN5jNd2379ggmHp4Xplmt4e"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
