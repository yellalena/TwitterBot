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
	#print(ascii(result))

	return result


def ShortenTweet(Tweet):
	Tweet = re.sub(', ', ',', Tweet)
	Tweet = re.sub(' - ', '-', Tweet)

	while(len(Tweet)>140):
		while Tweet[-1]!='.':
			Tweet = Tweet[:-1]


def Tweet(stringToReplace, replacement):
	aString = re.sub('"', '', stringToReplace)
	toReplace = re.compile(re.escape(str(aString)), re.IGNORECASE)
	print(toReplace)
	tweet = tweepy.Cursor(api.search, q=stringToReplace).items(10)

	for tw in tweet:
		txt=''
		tweetText = toReplace.sub(replacement, tw.text)
		#print(ascii(tweetText))
		txt = clearTweet(tweetText, txt)

		if (len(txt)>140):
			ShortenTweet(txt)

		#print(ascii(txt))
		
		try:
			api.update_status(txt.lower())
			print("Posted a tweet! '", txt, "'")
			time.sleep(240)
		except tweepy.error.TweepError as te:
			print (te)

if __name__=="__main__":
	#Tweet('"гулять по воде"', 'программировать')
	Tweet(sys.argv[1], sys.argv[2])

