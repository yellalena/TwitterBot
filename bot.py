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
	numbers = sys.argv[3] + sys.argv[4]
	numbers = re.findall('\d+', numbers)
	toReplace = re.compile(re.escape(str(stringToReplace)), re.IGNORECASE)
	tweet = tweepy.Cursor(api.search, q=('"'+stringToReplace+'"')).items(int(numbers[0])) # !CHOOSE HOW MANY TWEETS DO YOU WANT TO POST HERE

	for tw in tweet:
		txt=''
		tweetText = toReplace.sub(replacement, tw.text)
		txt = clearTweet(tweetText, txt)

		if (len(txt)>140):
			ShortenTweet(txt)
		
		try:
			api.update_status(txt.lower())
			try: 
				with open('log.txt', 'a') as log:
					log.write(" \n" + time.asctime() +" :: Posted a tweet: '" + txt + "' ")
			except UnicodeEncodeError:
				with open('log.txt', 'a') as log:
					log.write(" \n" + time.asctime() +" :: Posted a tweet containing an emoji. ") # logging in ascii is no-good for cyrillic, so decided not to log "emoji" tweets at all

			time.sleep(int(numbers[1])) # !CHOOSE THE PERIOD OF TWEETING HERE
		except tweepy.error.TweepError as te:
			with open('log.txt', 'a') as log:
				log.write(" \n" + time.asctime() +" :: "+ str(te))

if __name__=="__main__":
	Tweet(sys.argv[1], sys.argv[2])