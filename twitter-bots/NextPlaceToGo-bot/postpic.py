import tweepy
import os
import logging
from config import create_api


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def post_pic(api, img_path, status):
    logger.info(f"Uploading image {os.path.basename(img_path)}")
    try:
        api.update_with_media(img_path, status)
    except FileNotFoundError:
        print("File not found. Please check your file path.")


def main():
    api = create_api()

    img_path = "C:\\Users\\asus\\PythonScripts\personal-projects\\twitter-bots\\NextPlaceToGo-bot\\images\\bali.jpg"
    status = "Bali"

    # post pic
    post_pic(api, img_path, status)


if __name__ == '__main__':
    main()
