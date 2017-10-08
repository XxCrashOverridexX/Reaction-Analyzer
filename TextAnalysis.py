import urllib.request
import json

continueOn = True
while continueOn == True:
	# Configure API access
	apiKey = 'df07acba6d4e4ef69b3c994108ada4e9'
	sentimentUri = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment'
	keyPhrasesUri = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases'
	languageUri = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/languages'

	# Ask the user for a text

	gotResponse = False

	while gotResponse == False:
		print('Describe how you felt throughout the video:\n')
		sampleText = input()
		sampleTextNoSpace = sampleText.replace(" ", "")
		if len(sampleTextNoSpace) == 0:
			print("Sorry, that's not a valid response. Please try again.")
			gotResponse = False
		else:
			gotResponse = True
		
		

	# Prepare headers
	headers = {}
	headers['Ocp-Apim-Subscription-Key'] = apiKey
	headers['Content-Type'] = 'application/json'
	headers['Accept'] = 'application/json'


	# Detect language
	postData1 = json.dumps({"documents":[{"id":"1", "text":sampleText}]}).encode('utf-8')
	request1 = urllib.request.Request(languageUri, postData1, headers)
	response1 = urllib.request.urlopen(request1)
	response1json = json.loads(response1.read().decode('utf-8'))
	language = response1json['documents'][0]['detectedLanguages'][0]['iso6391Name'] # Sample json: {'errors': [], 'documents': [{'id': '1', 'detectedLanguages': [{'name': 'English', 'score': 1.0, 'iso6391Name': 'en'}]}]}
	 
	# Determine sentiment
	postData2 = json.dumps({"documents":[{"id":"1", "language":language, "text":sampleText}]}).encode('utf-8')
	request2 = urllib.request.Request(sentimentUri, postData2, headers)
	response2 = urllib.request.urlopen(request2)
	response2json = json.loads(response2.read().decode('utf-8'))
	sentiment = response2json['documents'][0]['score'] # Sample json: {'errors': [], 'documents': [{'id': '1', 'score': 0.946106320818458}]}
	 
	# Determine key phrases
	postData3 = postData2
	request3 = urllib.request.Request(keyPhrasesUri, postData3, headers)
	response3 = urllib.request.urlopen(request3)
	response3json = json.loads(response3.read().decode('utf-8'))
	keyPhrases = response3json['documents'][0]['keyPhrases'] # Sample json: {'documents': [{'keyPhrases': ['Azure'], 'id': '1'}], 'errors': []}

	#Display results
	print('Text: %s' % sampleText)
	print('Language: %s' % language)
	print('Sentiment: %f' % sentiment)
	print('Key phrases: %s' % keyPhrases)
	

	#ask if try again
	haveAnswer = False

	while haveAnswer == False:
		print("Would you like to give it another shot? (Yes/No)\n")
		tryAgain = str(input())
		if ((tryAgain == "Yes") or (tryAgain == "yes") or (tryAgain == "y") or (tryAgain == "Y") or (tryAgain == "Yea") or (tryAgain == "yea") or (tryAgain == "Sure") or (tryAgain == "sure")):
			haveAnswer = True
			continueOn = True
		elif ((tryAgain == "No") or (tryAgain == "no") or (tryAgain == "Nah") or (tryAgain == "nah")):
			haveAnswer = True
			continueOn = False
			print("Thanks for playing!")
		else:
			print("Sorry, something doesn't work, but it's not your fault.")
			haveAnswer = True
			continueOn = False

	