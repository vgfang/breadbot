# bot.py
import os
import random
import discord
import imgkit
import asyncio
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
randomWordsNum = 2

@bot.event
async def on_ready():
	for guild in bot.guilds:
		print(
			f'{bot.user} is connected to the following guild:\n'
			f'{guild.name}(id: {guild.id})'
		)

# generate random permuation of word_num separated by " "
def generate_name(wordNum:int) -> str:
	file = open("./words.txt", 'r')
	allWords = file.read().split('\n')
	selectedWords = random.sample(allWords, wordNum)
	return f'{selectedWords[0]} {selectedWords[1]} Bread'

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

	breadname = generate_name(randomWordsNum)
	filename = f"{recipePath}{breadname}-{flourGrams}g"

	recipeHtml = breadbot.generate_recipe(breadname, filename+".html", flourGrams)
	options = {'width': 700, 'disable-smart-width': ''}
	imgkit.from_string(recipeHtml, filename+".png", options=options)
	await ctx.send(file=discord.File(filename+".png"))
	await ctx.send(file=discord.File(filename+".html"))
	os.remove(filename+".png")
	os.remove(filename+".html")

bot.run(TOKEN)
