import snscrape.modules.twitter as sntwitter
import csv

maxTweets = 100000

with open('tweets_polswe.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # sntwitter.TwitterSearchScraper()
    writer.writerow(["username", "content", "date", "userlocation", "likecount", "retweetcount", "followers", "url"])
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(' lang:"pl" since:2021-06-21 until:2021-06-25 #POLSWE').get_items()):
        if i > maxTweets:
            break
        writer.writerow([tweet.username, tweet.content,
                         tweet.date, tweet.user.location,tweet.likeCount,
                         tweet.retweetCount, tweet.user.followersCount, tweet.url])
        # print(tweet.content)
