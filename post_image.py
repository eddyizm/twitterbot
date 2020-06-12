import os
import json
import tweepy
from glob import glob
import time
import urllib.request as req
from random import randrange, shuffle

CONFIG = r"C:\Users\eddyizm\HP\config.json"
SEARCH_LOG = r'search.json'


def check_for_tags(folder: str):
    tag = os.path.join(folder, 'tags.nfo')
    if os.path.exists(tag):
        with open(tag, 'r') as x:
            print(x.readlines())


def get_random_quote():
    ''' get random quote to use as tweet '''
    try:
        data = json.load(req.urlopen('https://eddyizm.com/quotes/random/'))
        # TODO count characters to check if quote is too long and if so loop for another one
        return data[0]['quote']
    except Exception as ex:
        print(ex)


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
            # print(os.path.dirname(filename))
            fullpath = filename
            break  # get first directory if it exists
    foldertag = os.path.basename(os.path.dirname(fullpath))
    return fullpath, foldertag


def tweet_photos(api, imagepath, text):
    status = f'#{text} #eddyizm | https://eddyizm.com'
    x = imagepath
    try:
        api.update_with_media(filename=x, status=status)
        print(f' {imagepath} Tweeted successfully!')
        # TODO try to post to IG, then delete
        os.remove(imagepath)
    except Exception as e:
        print(f'encountered error! error deets: {e}')


def get_folder():
    settings = get_keys()
    if os.name == 'nt':
        return settings["windows"]["image_path"]
    else:
        return settings["linux"]["image_path"]


def search_twtr(api, search_term):
    ''' search hashtag and save results, username and tweet to json '''
    data = {}
    try:
        print(f'searching term: {search_term}')
        for tweet in api.search(q=search_term, lang="en", count=5):
            print(f"{tweet.user.name}:{tweet.text}")
            data.update({tweet.user.name: tweet.text})
        save_search_results(data)
    except Exception as e:
        print(e)


def save_search_results(data):
    with open(SEARCH_LOG, 'w') as json_file:
        json.dump(data, json_file)


def main():
    time.sleep(randrange(1,3000))
    twitter_api = tweepy_creds()
    photo = get_images(get_folder())
    tweet_photos(twitter_api, photo[0], photo[1])
    # search_twtr(twitter_api, photo[1])


if __name__ == "__main__":
    # check_for_tags(r'C:\Users\eddyizm\HP\images\RedRocksBouldering')
    main()

