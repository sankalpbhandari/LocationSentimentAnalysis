#! /usr/bin/python3
import csv
import re
import time
import folium
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm import tqdm


class SentimentAnalysis:
    def __init__(self):
        self.map_all = folium.Map(location=[20, 0], tiles="Mapbox Bright", zoom_start=2)
        self.map_neu = folium.Map(location=[20, 0], tiles="Mapbox Bright", zoom_start=2)
        self.map_pos = folium.Map(location=[20, 0], tiles="Mapbox Bright", zoom_start=2)
        self.map_neg = folium.Map(location=[20, 0], tiles="Mapbox Bright", zoom_start=2)
        self.tweets = []

    def __filter_data(self, tweet):
        tweet.replace('\n', ' ')
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        return tweet.lower()

    def tweet_analysis(self):
        print("Analyzing Tweets")
        for i in tqdm(range(len(self.tweets)), ascii="Tweet Analysis"):
            sid = SentimentIntensityAnalyzer()
            tweet_polarity_score = sid.polarity_scores(self.tweets[i]['Tweet content'])
            self.tweets[i]['sentiment_compound_polarity'] = tweet_polarity_score['compound']
            self.tweets[i]['sentiment_neutral'] = tweet_polarity_score['neu']
            self.tweets[i]['sentiment_negative'] = tweet_polarity_score['neg']
            self.tweets[i]['sentiment_pos'] = tweet_polarity_score['pos']
            if self.tweets[i]['sentiment_compound_polarity'] > 0:
                self.tweets[i]['sentiment_type'] = 'POSITIVE'
                self.tweets[i]['color'] = 'green'

            elif self.tweets[i]['sentiment_compound_polarity'] == 0:
                self.tweets[i]['sentiment_type'] = 'NEUTRAL'
                self.tweets[i]['color'] = 'gray'

            elif self.tweets[i]['sentiment_compound_polarity'] < 0:
                self.tweets[i]['sentiment_type'] = 'NEGATIVE'
                self.tweets[i]['color'] = 'red'

    # def word_cloud(self):
    #     all_words = " "
    #     for i in range(len(self.tweets)):
    #         all_words += self.tweets[i]['Tweet content']
    #     from wordcloud import WordCloud
    #     import matplotlib.pyplot as plt
    #     wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110,
    #                           stopwords={"apple", "iphone", "0apple"}).generate(all_words)
    #     print(all_words)
    #     plt.figure(figsize=(10, 7))
    #     plt.imshow(wordcloud, interpolation="bilinear")
    #     plt.axis('off')
    #     plt.show()

    def read_tweet_csv(self):
        print("Reading CSV")
        with open('data/Apple_tweets_filtered.csv', encoding="ISO-8859-1") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for tweets in csv_reader:
                if line_count == 0:
                    line_count += 1
                elif tweets[2]:
                    tweet_d = dict()
                    tweet_d.update({'Tweet content': self.__filter_data(tweets[1])})
                    tweet_d.update({'Latitude': float(tweets[2])})
                    tweet_d.update({'Longitude': float(tweets[3])})
                    tweet_d.update({'color': 'grey'})
                    self.tweets.append(tweet_d)

    def create_map(self):
        print("Creating Map")
        for i in tqdm(range(len(self.tweets)), ascii="Map Creation"):
            color = self.tweets[i]['color']
            try:
                folium.Circle(radius=5000, location=[self.tweets[i]['Latitude'], self.tweets[i]['Longitude']],
                              popup=self.tweets[i]['Tweet content'], fill=True, color=color, fill_opacity=0.6,
                              fill_color=color, weight=2).add_to(self.map_all)
                if color == 'red':
                    folium.Circle(radius=5000, location=[self.tweets[i]['Latitude'], self.tweets[i]['Longitude']],
                                  popup=self.tweets[i]['Tweet content'], fill=True, color=color, fill_opacity=0.6,
                                  fill_color=color, weight=2).add_to(self.map_neg)
                elif color == 'green':
                    folium.Circle(radius=5000, location=[self.tweets[i]['Latitude'], self.tweets[i]['Longitude']],
                                  popup=self.tweets[i]['Tweet content'], fill=True, color=color, fill_opacity=0.6,
                                  fill_color=color, weight=2).add_to(self.map_pos)
                else:
                    folium.Circle(radius=5000, location=[self.tweets[i]['Latitude'], self.tweets[i]['Longitude']],
                                  popup=self.tweets[i]['Tweet content'], fill=True, color=color, fill_opacity=0.6,
                                  fill_color=color, weight=2).add_to(self.map_neu)
            except Exception as e:
                print(e)
                exit(0)
        # Save it as html
        try:
            self.map_all.save('data/all_tweets.html')
            self.map_neu.save('data/neutal_tweets.html')
            self.map_pos.save('data/positive_tweets.html')
            self.map_neg.save('data/negative_tweets.html')

        except Exception as e:
            print(e)


if __name__ == "__main__":
    start_time = time.time()
    a = SentimentAnalysis()
    a.read_tweet_csv()
    print(time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))
    # a.word_cloud()
    a.tweet_analysis()
    print(time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))
    a.create_map()
    print('The Map is ready\nPlease open "index.html" located in website folder')
    print(time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))
