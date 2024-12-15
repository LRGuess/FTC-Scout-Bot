import discord
import requests
import os
from dotenv import load_dotenv
from Pages.paginator import Paginator

load_dotenv()
URL = os.getenv('URL')
universal_footer = os.getenv('UNI_FOOTER')

async def season_info(ctx: discord.Interaction, *, team_number: int, season: int = 2024):
    await ctx.response.defer()

    query = '''
    query teamByNumber {
        teamByNumber(number: ''' + str(team_number) +''') {
            quickStats(season: ''' + str(season) + ''') {
                tot{value, rank},
                auto{value, rank},
                dc{value, rank},
                eg{value, rank},
                count
            }
        }
    }
    '''

    response = requests.post(URL, json={'query': query})
    data = response.json()

    try:
        teamByNumber = data['data']['teamByNumber']
    except:
        teamByNumber = None
    
    if teamByNumber == None:
        embed = discord.Embed(title="Team # not found", description="Please enter a valid team number", color=0xfc585b)
        embed.set_footer(text=universal_footer)
        await ctx.followup.send(embed=embed)
        return
    
    quickStats = data['data']['teamByNumber']['quickStats']
    if quickStats:
        total = quickStats['tot']
        autonomous = quickStats['auto']
        driver_control = quickStats['dc']
        end_game = quickStats['eg']
        count = quickStats['count']

        embed = discord.Embed(title=f"Season Stats for {team_number}", description=f":calendar_spiral:  Season: {season}", )
        if total:
            embed.add_field(name="Total Score:", value=f":1234: OPR: {round(total['value'], 3)} \n ---------- \n :medal: Rank: {total['rank']}", inline=False)
        if autonomous:
            embed.add_field(name="Auto:", value=f":1234: OPR: {round(autonomous['value'], 3)} \n ---------- \n :medal: Rank: {autonomous['rank']}", inline=True)
        if driver_control:
            embed.add_field(name="TeleOp:", value=f":1234: OPR: {round(driver_control['value'], 3)} \n ---------- \n :medal: Rank: {driver_control['rank']}", inline=True)
        if end_game:
            embed.add_field(name="End Game:", value=f":1234: OPR: {round(end_game['value'], 3)} \n ---------- \n :medal: Rank: {end_game['rank']}", inline=True)

        if count:
            embed.add_field(name=f"Count:", value=f"Rank is out {count} teams", inline=False)
    else:
        embed = discord.Embed(title=f"Season Stats for {team_number}", description=f"No quick stats available for season {season}", color=0xfc585b)

    embed.set_footer(text=universal_footer)

    await ctx.followup.send(embed=embed)