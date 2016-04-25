import tweepy, sys, time, re, mykeys

CONSUMER_KEY = mykeys.CONSUMER_KEY
CONSUMER_SECRET = mykeys.CONSUMER_SECRET
ACCESS_KEY = mykeys.ACCESS_KEY
ACCESS_SECRET = mykeys.ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def clearTweet(tweetText, result):
	#----------------------- tweet cleaners ---------------------------
	reply = re.compile('@[A-z]*')
	hashtag = re.compile('#[A-z]*')
	link = re.compile('https://[a-z, 0-9, ./]*')
	#------------------------------------------------------------------
	for word in tweetText.split():
		exclusions = (reply.match(word) or word=='RT' or hashtag.match(word) or link.match(word))
		if not exclusions:
			result+=(word+' ')

	result = re.sub("\n", ".", result)

	return result


def ShortenTweet(Tweet):
	Tweet = re.sub(', ', ',', Tweet)
	Tweet = re.sub(' - ', '-', Tweet)

	while(len(Tweet)>140):
		while (Tweet[-1]!='.' and Tweet!=''):
			Tweet = Tweet[:-1]


def Tweet(stringToReplace, replacement):
	toReplace = re.compile(re.escape(str(stringToReplace)), re.IGNORECASE)
	tweet = tweepy.Cursor(api.search, q=('"'+stringToReplace+'"')).items(10) # !CHOOSE HOW MANY TWEETS DO YOU WANT TO POST HERE

	for tw in tweet:
		txt=''
		tweetText = toReplace.sub(replacement, tw.text)
		txt = clearTweet(tweetText, txt)

		if (len(txt)>140):
			ShortenTweet(txt)
		
		try:
			api.update_status(txt.lower())
			print("Posted a tweet! '", ascii(txt), "'") #posting in ascii because otherwise posting an emoji will cause a error. doesn't make any sense though, just for checkinng
			time.sleep(240) # !CHOOSE THE PERIOD OF TWEETING HERE
		except tweepy.error.TweepError as te:
			print (te)

if __name__=="__main__":
	Tweet(sys.argv[1], sys.argv[2])

