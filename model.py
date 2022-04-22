from nltk.sentiment import SentimentIntensityAnalyzer
# import nltk
# nltk.download('vader_lexicon')

def sentiment_scores(sentence):
	sid_obj = SentimentIntensityAnalyzer()
	sentiment_dict = sid_obj.polarity_scores(sentence)
	return sentiment_dict['pos']*100
sentence = "This organisation was awesome. I am so happy with the service."
print(sentiment_scores(sentence))

