import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
URL = 'https://api.ftcscout.org/graphql'

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.tree.command(name='ping')
async def ping(ctx: discord.Interaction):
    await ctx.response.defer()

    await ctx.followup.send('Pong!')

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}!')

bot.run(DISCORD_TOKEN, reconnect=True)