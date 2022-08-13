import os
from dotenv import load_dotenv
from datetime import datetime
import time
import logging
import tweepy
import rules
import tweet_db as db
import telegram as tel
import report
import multiprocessing

logging.basicConfig(level=logging.INFO, filename="retweet_log.log", filemode="a", 
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s" )
logger = logging.getLogger(__name__)

# load config
load_dotenv()
bearer_token = os.getenv('bearer_token')
consumer_key = os.getenv('api_key')
consumer_secret = os.getenv('api_secret')
access_token = os.getenv('oauth_access_token')
access_token_secret = os.getenv('oauth_access_secret')


# Create Client instance to connect to twitter API V2
# OAuth 2.0 Bearer Token (App-Only)
bear_client = tweepy.StreamingClient(bearer_token)
    

# Initiate Client Authentification 1a
# needed for retweets and likes
oa1_client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
    )


# get rules
def get_rules():
    rules = bear_client.get_rules()
    logger.info( f"Stream rules: {rules} ")
    return rules.data


# delete rules
def delete_rules(rules):
    if rules is None:
        return None
    
    # I don´t know why it works, but it works
    # If you know a better way for tuple unpacking here let me know on github
    # [StreamRule(value='radix OR #radix -is:retweet -is:quote', tag='radix', id='1555500321245462528'), ...
    for a,b,c in rules:
        response = bear_client.delete_rules(ids=c)
        logger.info(f"{response} Name: {a}")


# set rules
def set_rules():
    rule_value = rules.search_rules[rules.rule_number]["value"]
    rule_tag = rules.search_rules[rules.rule_number]["tag"]
    search_rules = tweepy.StreamRule(value=rule_value , tag=rule_tag)
    response = bear_client.add_rules(search_rules)
    logger.info(f"Set rule: {response}")


# To customize the processing of the stream data, StreamingClient needs to be subclassed.
class StreamClient (tweepy.StreamingClient):

    # This function works as an event listener
    # On every new tweet in the stream it executes
    # Find the source code here: https://github.com/tweepy/tweepy
    def on_tweet(self, tweet):
        author_id = tweet.data["author_id"]
        tweet_id = tweet.id
        date = datetime.now()
        if db.db_check_duplicates(tweet_id):
            logger.warning("Tweet id already exists")
        else:
            db.db_input_tweet_id(tweet_id=tweet_id,author_id=author_id, date=date)
            logger.info(f"New tweet ID added to DB: {tweet_id}")
            # data from DB is returned as tuple - we need tuple unpacking here
            for retweet_id, in db.db_get_tweet_id():
                logger.info(f"Next retweet by id: {retweet_id}")
                response_like = oa1_client.like(tweet_id=retweet_id, user_auth=True)
                response_retwt = oa1_client.retweet(tweet_id=retweet_id, user_auth=True)
                logger.info(f"New retweet and like executed with id: {response_like} \n {response_retwt}")
                
                db.db_update_retweeted(tweet_id=retweet_id, is_retweeted=True)


    def on_errors(self, status_code):
        if status_code == 420:
            # returning false in on_data disconnets the stream
            return False



def run_twitter():
    rules = get_rules()
    delete_rules(rules)
    set_rules()
    stream = StreamClient(bearer_token, wait_on_rate_limit=True)
    stream.filter(expansions="author_id")
    
def run_telegram():
    while True:
        report.count_retweets()
        time.sleep(10)
        tel.telegram_run()
        time.sleep(86590) # run every 24h - 10 sec sleep above
      

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_twitter)
    p2 = multiprocessing.Process(target=run_telegram)

    p1.start()
    p2.start()

    p1.join()
    p2.join()