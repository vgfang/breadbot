import random
import math
from fractions import Fraction
from datetime import datetime
from jinja2 import Template

# empty class for passing to template engine 
class Recipe:
	def __init__(self):
		return

# returns flour percent using flour type
def get_special_flour_percent(flourType: str, breadFlourPercent:int) -> int:
	if flourType == 'Hard Red Whole Wheat' or flourType == 'Hard White Wheat':
		percentages = [0,25,30,35,40,45,50]
		percentages = list(filter(lambda x: 100-breadFlourPercent >= x, percentages))
		return random.choice(percentages)
	elif flourType == 'Rye' and breadFlourPercent >= 75:
		percentages = [0,10,15,20]
		percentages = list(filter(lambda x: 100-breadFlourPercent >= x, percentages))
		return random.choice(percentages)
	else:
		percentages = [0,10,15,20,25.30]
		percentages = list(filter(lambda x: 100-breadFlourPercent >= x, percentages))
		return random.choice(percentages)

# returns multiplied spoon units from teaspoon fraction input, 3 tsp = 1 tbsp
def spoon_mult(tsp: Fraction(), multiplier: float) -> str:
	tsp *= Fraction(multiplier)
	spoonString = ""
	if tsp >= 3: # use tablespoons
		tablespoons = int(tsp // 3)
		remainder = (tsp % 3) / 3
		if tablespoons != 0:
			spoonString += f"{tablespoons} "
		if remainder.numerator != 0:
			spoonString += f"{remainder.numerator}/{remainder.denominator} "
		return f"{spoonString}tbsp"
	else:
		teaspoons = int(tsp // 1)
		remainder = tsp % 1
		if teaspoons != 0:
			spoonString += f"{teaspoons} "
		if remainder.numerator != 0:
			spoonString += f"{remainder.numerator}/{remainder.denominator} "
		return f"{spoonString}tsp"

# returns amount given the type of flavoring(spices) 
def get_flavor_amount(flavor: str, flourAmount: int) -> str:
	colorsDict = {}
	scale = 4 # floors to the 500g/scale for clean fractional multiplication
	multiplier = math.floor(flourAmount/500*scale) / scale
	# flavors in category
	red = ('Cardamom', 'Nutmeg','Hazelnut','Almond','Lemon Extract','Peppermint')
	blue = ('Cinnamon', 'Allspice')
	green = ('Vanilla', 'Instant Coffee')
	purple = ('Orange Zest', 'Lime Zest', 'Lemon Zest', 'Ginger')
	orange = ('Lavender', 'Hojicha', 'Matcha', 'Earl Grey', 'Oolong')
	# default possible teaspoon values list for flour = 500, 3 tsp = 1 tbsp
	redAmt = list(map(Fraction, [1/4, 1/2]))
	blueAmt = list(map(Fraction, [1/4, 1/2, 1]))
	greenAmt = list(map(Fraction, [1/2, 1, 3/2]))
	purpleAmt = list(map(Fraction, [2, 3, 9/2]))
	orangeAmt = list(map(Fraction, [9]))
	# random tablespoons
	colorsDict[red] = list(map(lambda x: spoon_mult(x, multiplier), redAmt))
	colorsDict[blue] = list(map(lambda x: spoon_mult(x, multiplier), blueAmt))
	colorsDict[green] = list(map(lambda x: spoon_mult(x, multiplier), greenAmt))
	colorsDict[purple] = list(map(lambda x: spoon_mult(x, multiplier), purpleAmt))
	colorsDict[orange] = list(map(lambda x: spoon_mult(x, multiplier), orangeAmt))

	for color in colorsDict.keys():
		if flavor in color:
			return random.choice(colorsDict[color])

	# print("Error in Flavor Input: " + flavor)
	return "get_flavor_amount wrong input"

# returns list of spices using number of spices
def get_spices(spicesNum: int) -> [str]:
	spicesList = ['Cinnamon', 'Allspice', 'Cardamom', 'Nutmeg']
	if spicesNum > len(spicesList):
		print("WARNING: spicesNum exceeds spices of num")
		return spicesList
	if spicesNum == 1:
		return random.sample(['Cinnamon', 'Cardamom'], 1)
	return random.sample(spicesList, spicesNum)


# check if extract is nut
def is_nut(extract: str) -> bool:
	nuts = ['Hazelnut','Almond']
	return extract in nuts

# checks if extract1 and extract2 are both allowed based on zest/extract same flavor
def zest_extract_same_flavor(extract1: str, extract2: str) -> bool:
	if extract1 == extract2:
		return False
	e1 = extract1.split(" ") # may need to change if new types are added
	e2 = extract2.split(" ")
	if len(e1) != 2 or len(e2) != 2:
		return False
	
	if e1[0]==e2[0] and 'Zest' in [e1[1],e2[1]] and 'Extract' in [e1[1],e2[1]]:
		return True
	return False

# return list of extracts using number of extracts
def get_extracts(extractsNum: int) -> [str]:
	if extractsNum == 0:
		return []

	allowedExtracts = ['Vanilla', 'Hazelnut', 'Almond', 'Lemon Extract', 'Peppermint', 
		'Orange Zest', 'Lime Zest', 'Lemon Zest', 'Ginger']
	# if more than one, vanilla must be included
	currentExtracts = ['Vanilla']
	allowedExtracts.remove('Vanilla')
	extractsLeft = extractsNum-1
	
	while extractsLeft > 0:
		if len(allowedExtracts) <= 0:
			print("Incorrecnt number of extracts")
			return "Incorrecnt number of extracts"

		newExtract = random.choice(allowedExtracts)
		# one nut at a time
		if True in map(is_nut, currentExtracts) and is_nut(newExtract):
			allowedExtracts.remove(newExtract)
			continue # skips decrement, try again
		# no zest + extract comibination of the same flavor
		for currentExtract in currentExtracts:
			exit = False
			if zest_extract_same_flavor(currentExtract, newExtract):
				allowedExtracts.remove(newExtract)
				exit = True # skips decrement, try again
			if exit:
				continue

		# passed restraints, remove it from allowed
		currentExtracts.append(newExtract)
		if newExtract in allowedExtracts:
			allowedExtracts.remove(newExtract)
		extractsLeft -= 1
	return currentExtracts

# return percentage of enrichment
def get_enrichment_percent(enrichment: str) -> int:
	if enrichment == 'Cream Cheese':
		return 10
	return 5

# return liquid percent from liquid tpye
def get_liquid_percent(liquidType: str) -> int:
	if liquidType in ['Heavy Cream', 'Coconut Milk']:
		return 13
	elif liquidType in ['Cow Milk']:
		return 63
	# print("Error in liquidType input.")
	return -1

# return fruit puree fruit choice(s), omitted fruit chance weighting for now
def get_fruit_purees() -> [str]:
	fruitPureesNum = random.randint(1,2)
	fruitPureesChoices = ['Banana','Apple','Cherry','Strawberry','Fig','Mango']
	return random.sample(fruitPureesChoices, fruitPureesNum)

# retrun fruit puree percent from 0-2 fruitPurees using random generation 
def get_fruit_purees_percent(fruitPurees) -> [float]:
	totalFruitPureePercent = random.choice([25,30,35,40,45,50])
	fruitPureeNum = len(fruitPurees)
	if fruitPureeNum == 1:
		return [totalFruitPureePercent]
	elif fruitPureeNum == 2:
		firstPercent = random.randint(0,totalFruitPureePercent)
		return [firstPercent, totalFruitPureePercent - firstPercent]
	return [0]

# returns rounded ml conversion from percent, used in template
def to_g(flourMl, percent) -> int:
	return round(flourMl * percent/100)

# takes filename and writes an html recipe file
def generate_recipe(breadname: str, filename: str, flourGramInput: int) -> str:
	# ALL NUMBERICAL VALUES REPRESENT PERCENTAGES
	r = Recipe()
	r.breadname = breadname
	r.totalFlourGrams = flourGramInput
	r.totalLiquidPercent = 63

	r.preferment = random.choice(['Poolish', 'None'])
	r.breadFlourPercent = random.choice([75, 50])
	# FLOUR STYLE 
	r.breadShape = random.choice(['Pullman', 'Regular'])
	# FLOUR TYPES
	r.specialFlour = random.choice([
		'Einkorn',
		'Khorasan',
		'Spelt',
		'Emmer',
		'Semolina (Durum)',
		'Hard Red Whole Wheat',
		'Regular Whole Wheat',
		'Hard White Wheat',
		'Rye'
	])
	r.specialFlourPercent = get_special_flour_percent(r.specialFlour, r.breadFlourPercent)
	r.whiteFlourPercent = 100 - r.breadFlourPercent - r.specialFlourPercent

	# SPICES/FLAVORING
	spicesNum = random.randint(0,4)
	r.spices = get_spices(spicesNum)
	extractsNum = random.randint(0,3)
	r.extracts = get_extracts(extractsNum)
	teaList = ['Lavender', 'Hojicha', 'Matcha', 'Earl Grey', 'Oolong', 'Instant Coffee']
	r.tea = random.choice(teaList)
	# illegal with fruit purees and all extracts but ginger, almond, and hazelnut

	# BASIC INGREDIENTS
	r.sugar = random.choice(['Brown Sugar','White Sugar','Honey','Molasses'])
	r.sugarPercent = random.choice([5,10,15])
	r.salt = 'Table Salt'
	r.saltPercent = random.choice([1,1.5,2])
	r.yeast = random.choice(['Instant Yeast','Active Yeast'])
	r.yeastPercent = 0.62

	# ENRICHMENTS – All 5% , only one chosen
	enrichmentList = ['Olive Oil','Butter','Cream Cheese','Coconut oil']
	if r.tea == 'Instant Coffee':
		enrichmentList.remove('Olive Oil')
	r.enrichment = random.choice(enrichmentList)
	r.enrichmentPercent = get_enrichment_percent(r.enrichment)
	if r.enrichment == 'Cream Cheese':
		r.totalLiquidPercent -= 5
		
	# LIQUIDS
	# cap total liquid at 60% when these sugars are used
	if r.sugar in ['Honey', 'Molasses']:
		r.totalLiquidPercent = 60
	# cow milk only if there is no preferemnt
	viableLiquids = ['Heavy Cream', 'Coconut Milk', 'Cow Milk']
	if r.preferment != 'None':
		viableLiquids.remove('Cow Milk')
	r.liquid = random.choice(viableLiquids)
	r.liquidPercent = get_liquid_percent(r.liquid)

	## LIQUIDS - FRUIT PUREE
	r.fruitPurees = []
	r.fruitPureesPercent = []
	if r.preferment != 'Poolish':
		# 50 percent chance to include
			# sugar reduction by 5 percent
			r.sugarPercent -= 5
			r.fruitPurees = get_fruit_purees()
			r.fruitPureesPercent = get_fruit_purees_percent(r.fruitPurees)

	# account for cow milk
	r.liquidPercent = min(r.liquidPercent, r.totalLiquidPercent - sum(r.fruitPureesPercent))
	r.waterPercent = max(0, r.totalLiquidPercent - sum(r.fruitPureesPercent) - r.liquidPercent)

	# BICOLOR ROLL
	r.isBicolorRoll = False
	if len(r.fruitPureesPercent) > 0 or r.tea in ['Lavender', 'Hojicha', 'Matcha', 'Earl Grey', 'Oolong']:
		r.isBicolorRoll = random.choice([True,False])

	# COCOA POWDER
	r.cocoaPowderPercent = 0
	cocoaPowderAllowedExtracts = ['Ginger', 'Almond', 'Hazelnut']
	if r.fruitPurees == [] and any(not x in cocoaPowderAllowedExtracts for x in r.extracts): # allowed
		if random.randint(0,2) == 0:
			r.tea = '' # removes tea
			r.cocoaPowderPercent = round(random.choice([5,10])/100 * r.whiteFlourPercent,1)
			r.whiteFlourPercent = round(r.whiteFlourPercent - r.cocoaPowderPercent,1)

	# WRITE FORMAT
	time = datetime.now()
	r.datetime = time.strftime('%A, %b %d %Y')
	templateFile = open("./template.html")
	templateString = templateFile.read()

	## Conversion to ml for percentages
	r.totalLiquidGrams = to_g(r.totalFlourGrams, r.totalLiquidPercent)
	r.breadFlourGrams = to_g(r.totalFlourGrams, r.breadFlourPercent)
	r.specialFlourGrams = to_g(r.totalFlourGrams, r.specialFlourPercent)
	r.whiteFlourGrams = to_g(r.totalFlourGrams, r.whiteFlourPercent)
	r.sugarGrams = to_g(r.totalFlourGrams, r.sugarPercent)
	r.saltGrams = to_g(r.totalFlourGrams, r.saltPercent)
	r.yeastGrams = to_g(r.totalFlourGrams, r.yeastPercent)
	r.spicesAmt = list(map(lambda x: get_flavor_amount(x, r.totalFlourGrams), r.spices))
	r.extractsAmt = list(map(lambda x: get_flavor_amount(x, r.totalFlourGrams), r.extracts))
	r.teaAmt = get_flavor_amount(r.tea, r.totalFlourGrams)
	r.enrichmentGrams = to_g(r.totalFlourGrams, r.enrichmentPercent)
	r.waterGrams = to_g(r.totalFlourGrams, r.waterPercent)
	r.liquidGrams = to_g(r.totalFlourGrams, r.liquidPercent)
	r.fruitPureesGrams = list(map(lambda x: to_g(r.totalFlourGrams,x), r.fruitPureesPercent))
	r.cocoaPowderGrams = round(r.cocoaPowderPercent/100 * r.totalFlourGrams)

	'''
	## Preferment Changes
	if r.preferment == 'Poolish':
		r.breadFlourGrams //= 2
		r.specialFlourGrams //= 2
		r.whiteFlourGrams //= 2
		r.breadFlourPercent /= 2
		r.specialFlourPercent /= 2
		r.whiteFlourPercent /= 2
		r.waterGrams //= 2
		r.waterPercent /= 2
	'''

	template = Template(templateString)
	htmlString = template.render(r = r)
	outfile = open(f'{filename}', 'w')
	outfile.write(htmlString)
	outfile.close()
	templateFile.close()

	return "Success"

'''
TODO
- unit conversions?
- mechanism to delete old stuff

TESTS 
- preferment (poolish value change)
- cocoa powder
- tablespoon conversions
- bot integration

DONE
- writing to file
- cow milk
- liquid, cream cheese, fruit puree
- zest/extract check
'''
