#Importing necessary packages

from termcolor import colored
from pyfiglet import figlet_format
import requests
import random
import json

#Welcome text is written

figlettext = figlet_format("NutrApi 1.1","slant")
color_figlettext = colored(figlettext,"cyan")
print(color_figlettext)

# Printing an informative text

print("Hi there! Nutrapi will help you balance your diet with telling you how balanced your last daily intake was. Please type in all the food you had in a complete day. If you are younger than 18, pregnant or lactating, please directly consult to a professional.")

#Getting user input on weight and sex.

user_weight = float(input("Please type in your weight in kilograms: "))
user_sex = input("Please choose your sex with typing in M for male, F for female, or D if you don't want to share it or if you are not identifying with the sexes listed. In that case averages of male and and female values for nutritional references will be used for the calculations. For better precision please choose a sex: ").upper()


stop_of_the_list_cue = 0
food_list = []

#A loop that fills in the food list, using the user input in a query with the help of using USDA Api 

while stop_of_the_list_cue == 0:
#User input is taken	
	user_input = input("Tell us what you've consumed:")
# Query search using the USDA Api
	url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key=BOT5UpIZuRfB8BF1k5RYrD0njW01STrXdUIL3bKM&query={user_input}"

	response = requests.get(url).json()

	for i in response["foods"]:
		print(i["description"])
	second_input = input("Which one describes the item best? ")
	for e in response["foods"]:
		if e["description"] == second_input:
			food_item = e
			food_list.append(food_item)
	print (f'You\'ve chosen: {food_item["description"]}')
	continuation_request = input("Do you want to add other foods/drinks? Y/N:").upper()
	request_safety = 0
	while request_safety == 0:
		if continuation_request == "N":
			stop_of_the_list_cue = 1
			request_safety = 1
		elif continuation_request == "Y":
			request_safety = 1
		else:
			print('Please either type "Y" for yes or "N" for no!').upper
			request_safety = 0
			continuation_request = input("Do you want to add other foods/drinks? Y/N:").upper()
# An empty list gets initiated and gets filled in with the ingredient info selected from food_list
nutrientslist = []
for i in food_list:
	nutrientslist.append(i['foodNutrients'])

# The nutrients get isolated and stored in a list called nutrlist

nutrlist = []
for i in nutrientslist:
	for nutrient in i:
		nutrlist.append({nutrient["nutrientName"]:nutrient["value"]})
#The nutrients of interest are put in a dictionary, as well as their minimum and maximum reference values for each sex.
nutrients_dict = {"Protein": 0, "Fat": 0, "Vitamin C": 0, "Vitamin B1": 0, "Vitamin B2": 0, "Vitamin B3": 0, "Vitamin B5": 0, "Vitamin B6": 0,"Vitamin B9": 0,"Folate": 0, "Vitamin D": 0, "EPA & DHA": 0}
minimum_amount_male = {"Protein": user_weight * 0.8, "Fat": 44.0, "Vitamin C": 65.0, "Vitamin B1": 1.20, "Vitamin B2": 1.3, "Vitamin B3": 16, "Vitamin B5": 5, "Vitamin B6": 1.3,"Vitamin B9": 400,"Folate": 2.4, "Vitamin D": 20.0, "EPA & DHA": 250}
minimum_amount_female = {"Protein": user_weight * 0.8, "Fat": 44.0, "Vitamin C": 65.0, "Vitamin B1": 1.10, "Vitamin B2": 1.1, "Vitamin B3": 14, "Vitamin B5": 5, "Vitamin B6": 1.3,"Vitamin B9": 400,"Folate": 2.4, "Vitamin D": 20.0, "EPA & DHA": 250}
minimum_amount_diverse = {"Protein": user_weight * 0.8, "Fat": 44.0, "Vitamin C": 65.0, "Vitamin B1": 1.15, "Vitamin B2": 1.2, "Vitamin B3": 15, "Vitamin B5": 5, "Vitamin B6": 1.3,"Vitamin B9": 400,"Folate": 2.4, "Vitamin D": 20.0, "EPA & DHA": 250}
max_amount = {"Protein": user_weight * 2, "Fat": 77.0, "Vitamin C": 2000.0, "Vitamin B1": 50.0, "Vitamin B2": 400.0, "Vitamin B3": 50.0, "Vitamin B5": 10.000, "Vitamin B6": 100,"Vitamin B9":1000,"Folate": float("inf"), "Vitamin D": 100.0, "EPA & DHA": 3000}

#nutrient_dict gets updated with the nutrient values from the nutrlist

for i in nutrlist:
	if 'Protein' in i.keys():
		nutrients_dict["Protein"] += i['Protein']
	if 'Vitamin D (D2 + D3)' in i.keys():
		nutrients_dict["Vitamin D"] += i['Vitamin D (D2 + D3)']
	if 'Vitamin D (D2 + D3), International Units' in i.keys():
		nutrients_dict["Vitamin D"] += i['Vitamin D (D2 + D3), International Units']
	if 'Vitamin C, total ascorbic acid' in i.keys():
		nutrients_dict["Vitamin C"] += i['Vitamin C, total ascorbic acid']
	if 'Vitamin B-12' in i.keys():
		nutrients_dict["Folate"] += i['Vitamin B-12']
	if 'Thiamin' in i.keys():
		nutrients_dict["Vitamin B1"] += i['Thiamin']
	if 'Riboflavin' in i.keys():
		nutrients_dict["Vitamin B2"] += i['Riboflavin']
	if 'Niacin' in i.keys():
		nutrients_dict["Vitamin B3"] += i['Niacin']
	if 'Pantothenic acid' in i.keys():
		nutrients_dict["Vitamin B5"] += i['Pantothenic acid']
	if 'Vitamin B-6' in i.keys():
		nutrients_dict["Vitamin B6"] += i['Vitamin B-6']
	if 'Folate, total' in i.keys():
		nutrients_dict["Vitamin B9"] += i['Folate, total']
	if 'Vitamin B-12, added' in i.keys():
		nutrients_dict["Folate"] += i['Vitamin B-12, added']
	if 'PUFA 2:5 n-3 (EPA)' in i.keys():
		nutrients_dict["EPA & DHA"] += i['PUFA 2:5 n-3 (EPA)']
	if 'PUFA 22:6 n-3 (DHA)' in i.keys():
		nutrients_dict["EPA & DHA"] += i['PUFA 22:6 n-3 (DHA)']
	if 'Total lipid (fat)' in i.keys():
		nutrients_dict["Fat"] += i['Total lipid (fat)']
excessive_intake = []
lacking_intake = []
#total user intake gets evaluated for each nutrient. Cases where the amount of intake is more than the maximum or less than the minimum referance value are stored in lacking_intake and excessive_intake lists.
if user_sex == "M":
	for i in nutrients_dict.keys():
		if nutrients_dict[i] < minimum_amount_male[i] :
			lacking_intake.append(i)
		if nutrients_dict[i] > max_amount[i]:
		 	excessive_intake.append(i)
if user_sex == "F":
	for i in nutrients_dict.keys():
		if nutrients_dict[i] < minimum_amount_female[i] :
			lacking_intake.append(i)
		if nutrients_dict[i] > max_amount[i]:
		 	excessive_intake.append(i)
if user_sex == "D":
	for i in nutrients_dict.keys():
		if nutrients_dict[i] < minimum_amount_diverse[i] :
			lacking_intake.append(i)
		if nutrients_dict[i] > max_amount[i]:
		 	excessive_intake.append(i)

#User gets notified

if lacking_intake:
	print(f"If you typed in all your daily intake, you might be lacking these in your diet: {lacking_intake}")
	print("Please increase your intake or contact a professional.") 
if excessive_intake:
	print(f"If you typed in all your daily intake, you might be having too much of these in your diet: {excessive_intake}")
	print("Please decrease your intake or contact a professional.") 