NextPlaceToGo

A twitter bot that recommend people about places all around the wold. 

Functionality: 
1. Retweet: Retweet some tweets containing pictures that uses hashtags like: "travel", "vacation", "beach", etc 
   Implementation: actively watch for tweets that match certain criteria in real time. \
   This means that when there aren’t any new tweet matching the criteria, then the program will wait until a new tweet is created and then process it.
   Criteria for stream object: 
   - Is a tweet, not a comment / reply to someone else 
   - Could be a reply or mention to @NextPlaceToGo account 
   - Contain pictures 
   - Contain hashtags: #travel #vacation #beach #ocean #trip (tba)