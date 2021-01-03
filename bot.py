# bot.py
import os
import random
import discord
import imgkit
import bread as breadbot
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents=intents=discord.Intents.all()
intents = discord.Intents()
intents.members = True

bot = commands.Bot(command_prefix='!')

recipePath = './recipes/'

@bot.event
async def on_ready():
	for guild in bot.guilds:
		print(
			f'{bot.user} is connected to the following guild:\n'
			f'{guild.name}(id: {guild.id})'
		)

# checks if word in wordlist is valid for use
def invalid_word(word: str) -> bool:
	if word.isspace():
		return False
	if word == "":
		return False
	return True

# generate random name using word list in form "adjectve noun bread"
def generate_name() -> str:
	adjBreak = '> ADJECTIVES\\start\\below'
	nounBreak = '> NOUNS\\start\\below'

	file = open("./words.txt", 'r')
	text = file.read()
	textSplit = text.split(nounBreak + "\n")
	if len(textSplit) != 2:
		return f"Fix Improper WordList. Missing '{nounBreak}'."

	adjectives = textSplit[0].split('\n')
	if adjectives[0] != adjBreak:
		return f"Fix Improper WordList. Missing '{adjBreak}'."
	adjectives.remove(adjBreak)
	nouns = textSplit[1].split('\n')
	adjectives = list(filter(invalid_word, adjectives))
	nouns = list(filter(invalid_word, nouns))
	if len(nouns) == 0 or len(adjectives) == 0:
		return "Fix Improper WordList. Need at least one noun and adjective."

	adjective = random.choice(adjectives)
	noun = random.choice(nouns)

	return f'{adjective} {noun} bread'

# returns true if valid flour amount
def valid_flour_amount(flourAmt: str) -> int:
	if flourAmt is None:
		return False
	if not str(flourAmt).isnumeric():
		return False
	return True

@bot.command(name='bread', help='Responds with bread recipe with randomized parameters and optional flour grams.')
async def bread(ctx, flourGrams=500):
	if not valid_flour_amount(flourGrams):
		ctx.send("Improper flour grams input.")

	breadname = generate_name()
	filename = f"{recipePath}{breadname}-{flourGrams}g"

	recipeHtml = breadbot.generate_recipe(breadname, filename+".html", flourGrams)
	options = {'width': 700, 'disable-smart-width': ''}
	imgkit.from_string(recipeHtml, filename+".png", options=options)
	await ctx.send(file=discord.File(filename+".png"))
	await ctx.send(file=discord.File(filename+".html"))
	os.remove(filename+".html")
	os.remove(filename+".png")

bot.run(TOKEN)
