import datetime
import sqlite3
import logging
import pandas as pd
import random 
import rules

# logging config
logging.basicConfig(level=logging.INFO, filename="retweet_log.log", filemode="a", 
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
# set it to var logger
logger = logging.getLogger(__name__)

# connect to database
# use db location name -> :memory: for testing purposes
conn = sqlite3.connect("database.sqlite")
# create cursor to take action in the db
c = conn.cursor()

# create a table
# I use a dogstring for multiline commands
# If not run in memory comment it out after run once

c.execute('''CREATE TABLE IF NOT EXISTS retweets(
   tweet_id integers,
   is_retweeted integers,
   author integers,
   date text
      )''')


# create a table to store the daily tweet count data in it
c.execute('''CREATE TABLE IF NOT EXISTS tweetcount(
   tweet_count integers,
   date text
       )''')


# input tweet id and author
# author is needed for later checks if I am the author
def db_input_tweet_id(tweet_id, author_id, date, is_retweeted=False):
    with conn:
        c.execute("""INSERT INTO retweets 
                    VALUES (:tweet_id, :is_retweeted, :author, :date) """, 
                    {"tweet_id": tweet_id, "is_retweeted": is_retweeted, "author": author_id, "date":date})
        logger.info(f"New tweet ID added to DB: {tweet_id}")


# check if tweet id already exists
# delete second tweet id that is set to False
# can be used at table creating with UNIQUE
# But I don´t know how to skip this error and go to the next id
def db_check_duplicates(tweet_id):
    tweet_id_exists = False
    with conn:
        c.execute("""
                    SELECT * FROM retweets WHERE tweet_id = :tweet_id
        
                   """, {"tweet_id":tweet_id})

    # previos line select tweet_id of db only if the column contains the id
    if c.fetchone():
        return True
    else:
        return False


# get a all tweet id that haven´t been retweeted
def db_get_tweet_id():
    my_author_id = "1550155648796696578"
    with conn:
        try: 
            c.execute("""SELECT tweet_id FROM retweets 
                        WHERE is_retweeted = False
                        AND author != :my_author_id
                        """, {"my_author_id":my_author_id})
            id = c.fetchall()
            logger.info(f"Next tweet id up to retweet {id}")
            # returns value as tuple in a list
            return id

        except IndexError:
            logger.info("Currently no tweets to retweet")
        except:
            logger.warning("Can´t get tweet id from DB")

                  
# after retweet set tweed id to retweeted
def db_update_retweeted(tweet_id, is_retweeted):
    with conn:
        c.execute("""UPDATE retweets SET is_retweeted=:is_retweeted
                    WHERE tweet_id=:tweet_id
                    """, {"tweet_id": tweet_id, "is_retweeted": is_retweeted})
        logger.info(f"{tweet_id} is updated and retweet status set to: {is_retweeted}")


def show_all():
    with conn:
        c.execute('''
                    SELECT * FROM retweets
        
        ''')
        print(c.fetchall())


def delete_all(): # delete all except if already retweeted
    with conn:
        c.execute('''
                    DELETE FROM retweets WHERE is_retweeted = False
                    ''')
        logger.info("All DB entries deleted")

def df_get_all_retweets():
    df = pd.read_sql_query("SELECT * FROM retweets", conn)
    return df

def df_get_num_tweetcount():
    df = pd.read_sql_query("SELECT * FROM tweetcount WHERE date = '{}' ".format(datetime.date.today() - datetime.timedelta(days=rules.days_back)), conn)
    return df

def df_get_all_tweetcount():
    df = pd.read_sql_query("SELECT * FROM tweetcount ", conn)
    return df


def db_insert_retweet_count(tweet_count, date):
    with conn:
        c.execute("""
                        INSERT INTO tweetcount VALUES (?,?)
                        """, (tweet_count, date))


# after retweet set tweed id to retweeted
def testing_tweetcount():
    randlist = []
    for i in range(0,5):
        n = random.randint(2,6)
        randlist.append(n)

    for num in randlist:
        date = datetime.date.today() - datetime.timedelta(days=num)
        tweet_count = num * 6

        with conn:
            c.execute("""INSERT INTO tweetcount 
                            VALUES (:tweet_count, :date)
                        """, {"tweet_count":tweet_count, "date":date})

    logger.info(f"Test Date injected")



def delete_testdata():
    with conn:
        c.execute("DELETE FROM tweetcount")

