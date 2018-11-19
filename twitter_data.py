import json
import tweepy
import requests
from LocationSentimentAnalysis.authentication import Authentication


class TwitterData:
    def __init__(self):
        self.authen_o = Authentication()

    def __get_location(self, address):
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {'sensor': 'false', 'address': address, 'key': self.authen_o.get_google_key()}
        r = requests.get(url, params=params)
        results = r.json()['results']
        location = results[0]['geometry']['location']
        return [location['lat'], location['lng']]

    def fetch_tweets(self):
        try:
            auth = tweepy.OAuthHandler(self.authen_o.get_consumer_key(), self.authen_o.get_consumer_secret())
            auth.set_access_token(self.authen_o.get_access_token(), self.authen_o.get_access_token_secret())
            api = tweepy.API(auth)
            tweet_file = "data/apple_tweets.txt"
            file_p = open('data/apple_tweets.json', 'a')
            tweets = list()
            with open(tweet_file) as f:
                data = f.read().split()
                for tweet_id in data:
                    try:
                        tweet = api.get_status(tweet_id)
                        if tweet.coordinates:
                            tweets.append(tweet)
                        elif tweet.user.location:
                            tweet.coordinates = self.__get_location(tweet.user.location)
                            tweets.append(tweet)
                    except Exception as e:
                        print(e)
            json.dump(tweets, file_p)
            file_p.close()
        except Exception as e:
            print(e)
            exit(0)


if __name__ == "__main__":
    twitter_data_o = TwitterData()
    twitter_data_o.fetch_tweets()
