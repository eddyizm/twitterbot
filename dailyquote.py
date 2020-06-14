from post_image import tweepy_creds, get_daily_quote


def main():
    twitter_api = tweepy_creds()
    tweet = get_daily_quote()
    if tweet is not None:
        twitter_api.update_status(status=tweet)
        print(f'quote posted: {tweet}')
    else:
        print('quote too long, try again tomorrow!')


if __name__ == "__main__":
    main()
