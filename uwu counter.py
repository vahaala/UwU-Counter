import discord #imports Discord module
from discord.ext import commands #imports commands submodule from discord.ext
import os
from discord.utils import find #imports OS module
from dotenv import load_dotenv #imports load_dotenv submodule from dotenv
import json #imports json
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
intents = discord.Intents.all() #allows bot to basically work

def load_counter():
    with open("counter.json", "r") as f:
        counter = json.load(f)
    return counter

def save_counter(counter): 
    with open("counter.json", "w") as f:
        json.dump(counter, f)

load_dotenv() #loads .env file, which stores our Discord bot token. You probably will need to make one yourself, in the same spot as the script.

bot = commands.Bot(command_prefix = '_', intents = intents) #defines that this is a bot, and it's commands prefix

@bot.event #on bot event:
async def on_ready(): #when bot is fully ready:
    print("Successfully initiated {0.user}".format(bot)) #prints specified message in the console

@bot.event #sets up a bot event
async def on_message(ctx): #listens for messages
    if ctx.author.bot:
        return
    pattern = re.compile("uwu", re.IGNORECASE)
    global look
    look = pattern.findall(ctx.content)
    if len(look) > 0:
        counter = load_counter()
        counter["uwu"] += len(look)
        save_counter(counter)
    await bot.process_commands(ctx)

@bot.command()
async def count(ctx):
    counter = load_counter()
    await ctx.send(f"UwU's have been said {counter['uwu']} times on this server!")

@bot.command()
async def reset(ctx):
    counter = load_counter()
    counter["uwu"] = 0
    save_counter(counter)
    await ctx.send("UwU's counter has been reset and is now 0!")

bot.run(os.getenv("DISCORD_TOKEN"))