# bot.py
import os
import discord
import random
import uuid
import bread
from datetime import datetime
from jinja2 import Template
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
	if flourAmt == None:
		return False
	elif not str(flourAmt).isnumeric():
		return False
	return True

@bot.command(name='sandwich', help='Responds with bread recipe with randomized parameters and optional flour grams.')
async def sandwich(ctx, flourGrams=500):
	breadname = generate_name(randomWordsNum)
	filename = f"{recipePath}{breadname}-{flourGrams}g.html"

	msg = bread.generate_recipe(breadname, filename, flourGrams)
	if msg != "Success":
		await ctx.send("Error. Contact Bot maintainer.")
	await ctx.send(file=discord.File(filename))


bot.run(TOKEN)