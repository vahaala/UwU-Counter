import discord #imports Discord module
from discord.ext import commands #imports commands submodule from discord.ext
import os
from discord.utils import find #imports OS module
from dotenv import load_dotenv #imports load_dotenv submodule from dotenv
import json #imports json
import re

os.chdir(os.path.dirname(os.path.abspath(__file__))) #allows the json file to be readable by this bot
intents = discord.Intents.all() #allows bot to basically work

def load_counter(): #defines a function to load the json counter file
    with open("counter.json", "r") as f: #opens the file in read mode
        counter = json.load(f) #loads json contents
    return counter #returns json contents

def save_counter(counter): #defines a function to modify the json
    with open("counter.json", "w") as f: #opens the file in write mode
        json.dump(counter, f) #saves the json

load_dotenv() #loads .env file, which stores our Discord bot token. You probably will need to make one yourself, in the same spot as the script.

bot = commands.Bot(command_prefix = '_', intents = intents) #defines that this is a bot, and it's commands prefix

@bot.event #on bot event:
async def on_ready(): #when bot is fully ready:
    print("Successfully initiated {0.user}".format(bot)) #prints specified message in the console

@bot.event #sets up a bot event
async def on_message(ctx): #listens for messages
    if ctx.author.bot: #makes it so "uwu" said by bot won't be added to the counter
        return
    pattern = re.compile("uwu", re.IGNORECASE) #creates a RegEx pattern to look for "uwu", case insensitive
    global look #RegEx variable
    look = pattern.findall(ctx.content) #looks through the message for "uwu"
    if len(look) > 0: #if there are results:
        counter = load_counter() #opens json
        counter["uwu"] += len(look) #adds the amount of "uwu"s said to the counter variable inside json
        save_counter(counter) #saves the modified counter
    await bot.process_commands(ctx) #allows bot to process commands, since overriding on_message blocks this

@bot.command() #a simple command to print out how many "uwu"s were said so far
async def count(ctx):
    counter = load_counter() #loads json
    await ctx.send(f"UwU's have been said {counter['uwu']} times on this server!")

@bot.command() #a simple command to reset "uwu"s count
async def reset(ctx):
    counter = load_counter() #loads json
    counter["uwu"] = 0 #sets the counter var to 0
    save_counter(counter) #saves json
    await ctx.send("UwU's counter has been reset and is now 0!")

bot.run(os.getenv("DISCORD_TOKEN")) #runs the bot