# Stream Rules

## (giveaway OR #givaway OR airdrop OR #airdrop)
## has:hashtag
## (#giveaway OR giveaway)

# It´s best to test the rules in postman before applying them. For to generic
# rules the rate limit can be exceeded quickly

search_rules = [
        {"value": "#near (crypto OR nft OR blockchain OR #crypto) -is:retweet -is:quote -is:reply lang:en", "tag": "crypto & near"},
        {"value": "#radix -is:retweet -is:quote -is:reply", "tag": "radix"},
        {"value": "(crypto OR #crypto) (#giveaway OR giveaway) -is:retweet -is:quote -is:reply lang:en", "tag": "crypto giveaway & airdrops"}
    ]

# set the number to chooche a rule from above
# list indexes start with 0
rule_number = 0

# for the reporting tweet count
# set how many days you want to go back from today on
# date = today - days back you define
days_back = 1



