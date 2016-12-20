# * Created by Eliakah kakou
# Main.
# This class runs all of the modules in the right sequential
# order depending on the input

import tweepy
from time import sleep


# main method
def main():
    bot = TwitterBot("Z5dDoNOB1efZTIHsc3K39BTFa", "0OmTmSNH7whf7V06Z4LE3W4zXDAwxPKk9d948RLlQCBv7NgMyG",
                     "746388158-iY84sri3WGMULG9Hw3Q00ICurtA3pm8IMAho1gq7",
                     "H6oTFv58fmrkmaluiNTuBKxgpRnFK08hgtMH5c79u6ZEG")
    bot.getTweetsFromHash("finals")


# this class makes call to the twitter api
class TwitterBot:
    # contsructor
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key  # "Z5dDoNOB1efZTIHsc3K39BTFa"
        self.consumer_secret = consumer_secret  # "0OmTmSNH7whf7V06Z4LE3W4zXDAwxPKk9d948RLlQCBv7NgMyG"
        self.access_token = access_token  # "746388158-iY84sri3WGMULG9Hw3Q00ICurtA3pm8IMAho1gq7"
        self.access_token_secret = access_token_secret  # "H6oTFv58fmrkmaluiNTuBKxgpRnFK08hgtMH5c79u6ZEG"

    # this method prints the last 10 tweets from this hashtag
    def getTweetsFromHash(self, hashtag):

        hashtag = '#' + str(hashtag)

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)  # authorising your access, login
        auth.set_access_token(self.access_token, self.access_token_secret)  # set access token
        auth.secure = True  # make it secure = yes
        api = tweepy.API(auth)  # allows us to use the API

        print(hashtag)
        # this just fetches the most recent entries for #

        count = 1

        for tweet in tweepy.Cursor(api.search, q=hashtag, lang='en').items():
            if count == 11:
                break
            try:
                print("Tweet #" + str(count))
                print("Found tweet by: @" + tweet.user.screen_name)
                print("Found tweet by user_id: " + str(tweet.user.id))
                print("User Location: " + str(tweet.user.location))
                print("Saying: '" + tweet.text + "'\n")


            except tweepy.TweepError as e:
                print(e.reason)
                sleep(10)
                continue
            except StopIteration:
                break

            count += 1


main()  # main method call
