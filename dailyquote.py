from post_image import tweepy_creds, get_daily_quote


def main():
    twitter_api = tweepy_creds()
    tweet = get_daily_quote()
    if tweet is not None:
        twitter_api.update_status(status=tweet, attachment_url='https://eddyizm.com/quotes/')
        print(f'quote posted: {tweet[0]["quote"]}')


if __name__ == "__main__":
    main()
