import requests
import json
import base64

"""
##################################################
#--------------------NOTES------------------------#

#running this script requires the requests and twilio API libraries to be installed
#you can install these using pip

#for Twilio, since this script is using a trial account, your phone number needs to registered on my account to receive text messages
#just let me know if you want to try it out, otherwise just select to print the results to console.



##################################################
"""


print('Welcome to Jinyi\'s Hunger Helper app!')
print('If you\'re thinking of eating in, I will help you select a good recipe with your selected ingredients!')
print('If you\'re thinking of eating out, I will help you select a restaurant around the area!')
print('Either way I\'ll send you a text message with the results!')

print('')
print('To start off, in order to use Twilio (text messaging API), you must register your phone number with me, Jinyi, for verification purposes.')
print('')
print('Do you want to continue with Twilio or just console output?')
print('1: Twilio')
print('2: Just console')
twilioConsoleSelection=input('Please enter your selection: ')

print('')
print('Do you want to eat in or eat out today?')
print('')

eatInEatOut=4
while(eatInEatOut != str(1) and eatInEatOut !=str(2)):
	eatInEatOut=raw_input('Type 1 to eat in, 2 to eat out: ')



#--------------------Eat in - recipe branch -----------------------------------#
if eatInEatOut==str(1):
	print('OK! Let\'s eat in today.')
	print('')

	#Recipe puppy - Recipe search
	#http://www.recipepuppy.com/about/api/
	#make request with ingredients and dish type, receive list of recipes in response

	numIngredients=input('How many ingredients do you have today? -- Up to 10 or so: ')


	ingredients=[]

	for i in range(numIngredients):
		ingrInput=raw_input('Please enter ingredient ' + str(i+1) + ': ')
		ingredients.append(ingrInput)


	#print(ingredients)

	for i in range(len(ingredients)):
		if i==0:
			ingredientsQuery=ingredients[i]

		elif i>0:
			ingredientsQuery=(ingredientsQuery + ',' + ingredients[i])


	typeOfDish=raw_input('What type of dish do you want to make? -- pizza, omelet, stew, casserole, sandwich, burger,etc: ')


	url = "http://www.recipepuppy.com/api/"

	#print(ingredientsQuery)

	querystring = {"i":ingredientsQuery,"q":typeOfDish}
	payload=""

	response = requests.request("GET", url, data=payload, params=querystring)


	responseJSON=json.dumps(response.json())
	responseDICT=json.loads(responseJSON)


	#print(responseJSON)

	#print len(responseDICT["results"])

	print('')

	for i in range(len(responseDICT["results"])):
		print(str(i+1) + ': ' + responseDICT["results"][i]["title"].strip())


	print('')
	userSelection=raw_input('Let me know which one sounds good (1- ' + str(len(responseDICT["results"])) + '): ')

	userSelectionIndex=int(userSelection)-1

	


	"""
	#Twilio


	#Capture useful data from JSON response of previous API calls and send in a text message
	#Title of recipe, ingredients required, thumbnail, and link for more info.
	"""



	rTitle=responseDICT["results"][userSelectionIndex]["title"].strip()
	rIngredientsRequired=responseDICT["results"][userSelectionIndex]["ingredients"]
	rHyperlink=responseDICT["results"][userSelectionIndex]["href"]


	rimage_url=responseDICT["results"][userSelectionIndex]["thumbnail"]
	if rimage_url=="":
		rimage_url="https://us.123rf.com/450wm/alexraths/alexraths1506/alexraths150600035/41235288-blank-cookbook-and-spices-on-wooden-table.jpg?ver=6"

	textBodyLine1=('Requested recipe information:\n')
	textBodyLine2=('Title: ' + rTitle + '\n')
	textBodyLine3=('Ingredients required: ' + rIngredientsRequired + '\n') 
	textBodyLine4=('Source: ' + str(rHyperlink) + '\n')







	#-----------------------------Google maps API, return the nearest supermarket---------------------------#

	print('Got it!')
	print('But first: where are you located? This is so I can suggest a nearby supermarket to buy ingredients if you so choose!')
	userLocation=raw_input('You can respond with city name, abbrevations like NYC or LA, ZIP code, an address, etc: ')
	print('')

	userLocation=str(userLocation)

	#userLocation.replace(" ", "%20")

	astring64="QUl6YVN5RFA2YU5zaGJha2VmaFlfSDlDWTNwaGdJUTg0VWxKeWZj"
	astring=base64.b64decode(astring64)

	url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

	querystring = {"query":"supermarkets near " + userLocation, "key":astring}

	#print(querystring)

	payload = ""
	response = requests.request("GET", url, data=payload, params=querystring)

	responseJSON=json.dumps(response.json())
	responseDICT=json.loads(responseJSON)

	#print(responseDICT)

	nearestSupermarketName=responseDICT["results"][0]["name"]
	nearestSupermarketAddress=responseDICT["results"][0]["formatted_address"]


	textBodyLine5=("")
	textBodyLine6=('Your nearest supermarket is: ' + nearestSupermarketName + ' located at ' + nearestSupermarketAddress + '\n')



	textBodyIngredients=textBodyLine1+textBodyLine2+textBodyLine3+textBodyLine4+textBodyLine5+textBodyLine6

	print(textBodyIngredients)

	if twilioConsoleSelection==1:
			print('')
			print('Got it! I\'ll now send over the recipe details to your phone so you can have them on hand.')
			print('')

			userPhoneNumber=str(raw_input("Now please enter your phone number so I can send you the details: "))

			print('')
			print('Your text message with the recipe information should be received shortly. Bon Appetit!')



	print('')





#--------------------Eat out - restaurant branch ------------------------------#
if eatInEatOut==str(2):
	print('OK! Let\'s eat out today.')
	print('Where are you located?')
	userLocation=raw_input('You can respond with city name, abbrevations like NYC or LA, ZIP code, an address, etc: ')
	print('')


	#Yelp API - business search
	#https://www.yelp.com/developers/documentation/v3/business_search
	#this one returns a list of the best/most popular restaurants in an area

	url = "https://api.yelp.com/v3/businesses/search"

	querystring = {"location":userLocation,"limit":"5"}

	payload = ""
	headers = {
	    'Content-Type': "application/json",
	    'Authorization': "Bearer TPIIVWiBsWueYuVcrU7H4fdPOFjp1bF64vCkO3UxY0o-zwEAjJ7A00Qrile8DETiNDWCPGEdjmilSaZCfmy723stUbxhjY9wQAEZT93TVf7oK3UN3aqktfo1K1_oXHYx"
	    }

	response = requests.request("GET", url, data=payload, headers=headers, params=querystring)






	print('I selected five restaurants near your location at ' + userLocation + '.')


	responseJSON=json.dumps(response.json())
	responseDICT=json.loads(responseJSON)

	#print(responseDICT)

	#print(responseDICT["total"])
	#print(responseDICT["region"])
	#print(responseDICT["businesses"][0]) #*********** returns the first business in the list
	print('1: ' + responseDICT["businesses"][0]["name"]) 
	print('2: ' + responseDICT["businesses"][1]["name"])
	print('3: ' + responseDICT["businesses"][2]["name"])
	print('4: ' + responseDICT["businesses"][3]["name"])
	print('5: ' + responseDICT["businesses"][4]["name"])
	print('')





	userSelection=raw_input('Let me know which one sounds good (1-5): ')
	userSelectionIndex=int(userSelection)-1

	print('')

	if twilioConsoleSelection==1:
		print('Got it! I\'ll now send over the restaurant details to your phone so you can have them on hand.')

		userPhoneNumber=str(raw_input("Please enter your phone number so I can send you the details: "))

	else:
		print('Got it! Printing results to console: ')

	"""
	#Twilio

	#Capture useful data from JSON response of previous API calls and send in a text message
	#Name of restaurant, location, rating, phone number, image_url, price$$$,  etc.
	"""


	rName=responseDICT["businesses"][userSelectionIndex]["name"]

	rLocation=responseDICT["businesses"][userSelectionIndex]["location"]["display_address"] #location is in a list, have to combine into 1
	rLocationReadable=(rLocation[0] + ' ' + rLocation[1])

	rPhoneNum=responseDICT["businesses"][userSelectionIndex]["display_phone"]

	rCategories=responseDICT["businesses"][userSelectionIndex]["categories"]
	rCategoriesIndividual=''
	rCategoriesReadable=''

	maxLength= len(rCategories)
	#print(maxLength)
	#print(rCategories)
	i=0
	while i<maxLength:
		rCategoriesIndividual=responseDICT["businesses"][userSelectionIndex]["categories"][i]["title"]


		if i!=maxLength-1:
			rCategoriesReadable=(rCategoriesReadable + rCategoriesIndividual + ', ')

		else:
			rCategoriesReadable=(rCategoriesReadable + rCategoriesIndividual + '.')

		i+=1


	rRating=responseDICT["businesses"][userSelectionIndex]["rating"]
	rPrice=responseDICT["businesses"][userSelectionIndex]["price"]
	rimage_url=responseDICT["businesses"][userSelectionIndex]["image_url"]


	textBodyLine1=('Requested restaurant information:\n')
	textBodyLine2=('Name: ' + rName + '\n')
	textBodyLine3=('Location: ' + rLocationReadable + '\n') 
	textBodyLine4=('Phone Number: ' + rPhoneNum + '\n')
	textBodyLine5=('Categories: ' + rCategoriesReadable + '\n')
	textBodyLine6=('Rating: ' + str(rRating) + '\n')
	textBodyLine7=('Price: ' + rPrice + '\n')


	textBodyRestaurant=textBodyLine1+textBodyLine2+textBodyLine3+textBodyLine4+textBodyLine5+textBodyLine6+textBodyLine7

	print(textBodyRestaurant)

	print('')

	if twilioConsoleSelection==1:
		print('Your text message with the restaurant information should be received shortly. Bon Appetit!')
		#want to include in the body the restaurant details specified by the user.

	#print(message.sid)


#----Set text message body based on eating in or eating out
if eatInEatOut==str(1):
	textBody=textBodyIngredients

elif eatInEatOut==str(2):
	textBody=textBodyRestaurant


#-----------------Twilio-------------------#
from twilio.rest import Client


clientA1="QUNjN2NhZmI3ZGZlZmY2YmQwOTRkZWVhNzYyNDdhNjAxOQ=="
clientB1="ZTZhOWRiNGNhZGJkMWZkMTAzMzk2YWExOGMzYzRkNzc="


clientA2=base64.b64decode(clientA1)
clientB2=base64.b64decode(clientB1)

client = Client(clientA2, clientB2)

if twilioConsoleSelection==1:
	message = client.messages.create(
		to=userPhoneNumber,
		from_="+13232187649",
		body=textBody,
		media_url= rimage_url)


print('')







