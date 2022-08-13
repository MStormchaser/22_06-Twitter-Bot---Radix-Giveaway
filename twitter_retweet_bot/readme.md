# Introduction
This is a twitter retweet bot that creates an report every 24h about how many retweets happend the day before. After the numbers
are generated a line graph is plotted and with the numbers sent to a telegram bot. 

Via the twitter API a filtered stream is opened that continuely listens for new tweets by pre defined rules. Every new tweet data is stored in a sqlite database
to keep track of all retweets. Before inputing the new retweet data it checks if this tweet id already exists or the author is myself. After every successful entry
into the database the tweet will be retweeted and liked. The retweet status in the database is set to true after this. 

Every 24h the numbers of the retweets from the previous day are accumulated and stored in a seperate table. With keeping track of the retweets it is easily possible to create a daily report on how many tweets have been retweeted as well as creating a line plot. After creating the data it is sent to a telegram bot.

# Working with the files

To use those bots twitter and telegram credentials are required. Here you can sign up for a twitter developer account: https://developer.twitter.com/en
In order to obtain telegram api credentials for your bot go to telegram and search for **botfather** this is the twitter bot that creates you bot and creates your credentials. It also helps you to set up your bot.

1. Twitter:
This twitter bot uses two authentification methods. The bearer auth to create the stream and the OAuth 1a method to do operations for a specific user. In our case retweeting and liking. 

1.1 Create a bear auth token
1.2 Create OAuth 1a tokens
1.3 Get your author id (Use Postman and the "Search User by Name" function to obtain the author id)

2. Telegram:
This bot uses a simple token authentification method. It will be created in the telegram app by the botfather bot. https://core.telegram.org/
Get the chat id of the chat you like your bot to post to. 

3. Credential handling
Create a .env file to store you credentials. If you use the same variable name as in the files you only need to add your keys. 