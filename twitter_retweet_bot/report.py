import pandas as pd
import tweet_db as db
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import rules
import logging as log

# logging config
log.basicConfig(level=log.INFO, filename="retweet_bot/logs/retweet_log.log", filemode="a", 
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
# set it to var logger
logger = log.getLogger(__name__)


# count retweets from yesterday and add to 
# new table
def count_retweets():
    # create df from retweets
    df = db.df_get_all_retweets()
    # convert date to a datetime object in df
    df["date"] = pd.to_datetime(df["date"]).apply(lambda x: x.date())
    # create start & end time of the lookup range
    yesterday = datetime.date.today() - datetime.timedelta(days=rules.days_back)
    # filter the date
    df = df.loc[df["date"] == yesterday]
    # count rows
    number = len(df["date"])
    date = yesterday
    # add the retweets count from yesterday and date to it
    db.db_insert_retweet_count(number, date)
    log.info(f"Retweets from {date} counted: {number}")
    


def daily_count_plot():
    sns.set_style("whitegrid")
    df = db.df_get_all_tweetcount()
    df["tweet_count"] = df["tweet_count"].astype(int)
    sns.lineplot(x="date", y="tweet_count", data=df)
    time = datetime.date.today()
    plt.savefig(f"twitter_retweet_bot/plots/daily_count_plot_{time}.png")
    images = {}
    images["photo"] = open(f"twitter_retweet_bot/plots/daily_count_plot_{time}.png", "rb")
    log.info(f"Plot successfully created at: {time}")
    return images



def daily_nums():
    yesterday = datetime.date.today() - datetime.timedelta(days=rules.days_back)
    df = db.df_get_num_tweetcount()
    log.info(f"Tweet Count from {yesterday} succeffully completed.")
    return f"Retweets & likes from {yesterday} are: " + df["tweet_count"].to_string(index=False)  

