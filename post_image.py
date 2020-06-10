import os
import json
import tweepy
from glob import glob
# import requests
from random import shuffle

CONFIG = r'/home/eddyizm/HP/config.json'


def get_keys():
    with open(CONFIG, 'r') as myfile:
        keys = myfile.read()
        return json.loads(keys)


def tweepy_creds():
    settings = get_keys()
    consumer_key = settings['twitter']['api_key']
    consumer_secret = settings['twitter']['api_secret_key']
    access_token = settings['twitter']['access_token']
    access_token_secret = settings['twitter']['access_token_secret']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def get_images(folder: str):
    ''' get a list of image from a folder recursively and randomize before returning one for posting '''
    folders = glob(folder+'/**/*.jpg', recursive=True)
    shuffle(folders)
    fullpath = ''
    for filename in folders:
        if os.path.isfile(filename):
            fullpath = filename
            break  # get first directory if it exists
    foldertag = os.path.basename(os.path.dirname(fullpath))
    return fullpath, foldertag


def tweet_photos(api, imagepath, text):
    status = f'#{text} #eddyizm | https://eddyizm.com'
    x = imagepath
    try:
        api.update_with_media(filename=x, status=status)
        print('Tweeted! successfully')
        #TODO try to post to IG, then delete
        os.remove(imagepath)
    except Exception as e:
        print(f'encountered error! error deets: {e}')


def get_folder():
    settings = get_keys()
    if os.name == 'nt':
        return settings["windows"]["image_path"]
    else:
        return settings["linux"]["image_path"]


def main():
    twitter_api = tweepy_creds()
    photo = get_images(get_folder())
    tweet_photos(twitter_api, photo[0], photo[1])


if __name__ == "__main__":
    photo = get_images(get_folder())
    print(photo)
    print(photo[0], photo[1])
