import discord
import requests
import os
from dotenv import load_dotenv
from Pages.paginator import Paginator

load_dotenv()
URL = os.getenv('URL')
universal_footer = os.getenv('UNI_FOOTER')

async def matches_played(ctx: discord.Interaction, season: int = 2024):
    await ctx.response.defer()

    query = '''
        query matchesPlayed {
            matchesPlayedCount(season: ''' + str(season) + ''')
        }
    '''

    response = requests.post(URL, json={'query': query})
    data = response.json()

    matches_played = data['data']['matchesPlayedCount']

    embed = discord.Embed(title=f"Matches Played in {season}", color=0x00ff00)
    embed.add_field(name=f"{matches_played}", value="That's a lot!", inline=False)

    embed.set_footer(text=universal_footer)
    await ctx.followup.send(embed=embed)