import discord
import csv
from discord.ext import commands
import asyncio
import random
from threading import Event

intents = discord.Intents.default()
intents.message_content = True

randomMax = 16200 #4.5 hours
randomMin = 5400 #90 minutes

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)
exit = Event()

affirmationSet = {}
preferredName = None

def generate_wait_time():
    return random.randRange(randomMin, randomMax)

def init_affirmations(filename):
    with open(filename, newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        affirmationSet.update(csvreader)

@client.event()
async def on_ready():
    init_affirmations("affirmations.csv")
    print(f'AffirmationBot initialized and ready to go!')

async def main_loop(ctx):
    while not exit.is_set():
        await ctx.send(random.choice(affirmationSet).format(name = preferredName if preferredName else ctx.author.display_name))
        exit.wait(generate_wait_time())
    

@bot.command()
async def start(ctx):
    if exit.is_set():
        exit.clear()
        await ctx.send("AffirmationBot is starting up.")
        await main_loop(ctx)
    else:
        await ctx.send("AffirmationBot is already active!")

@bot.command()
async def stop(ctx):
    if not exit.is_set():
        exit.set()
        await ctx.send("AffirmationBot has been stopped.")
    else:
        await ctx.send("AffirmationBot is not currently running.")

@bot.command()
async def send(ctx):
    await ctx.send(random.choice(affirmationSet).format(name = preferredName if preferredName else ctx.author.display_name))

@bot.command(ctx)
async def help(ctx):
    await ctx.send(helpString)

@bot.command()
async def commands(ctx):
    help(ctx)