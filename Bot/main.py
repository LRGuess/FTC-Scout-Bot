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

universal_footer = "Made by Liam from 22212, FTC Scout API"

@bot.tree.command(name='ping')
async def ping(ctx: discord.Interaction):
    await ctx.response.defer()

    await ctx.followup.send('Pong!')

@bot.tree.command(name='teaminfo', description='Generalized team info')
async def team_info_by_number(ctx: discord.Interaction, *, team_number: int):
    await ctx.response.defer()

    query = '''
    query teamByNumber {
        teamByNumber(number: ''' + str(team_number) +''') {
            name
            schoolName
            sponsors
            location{
                venue
                city
                state
                country
            }
            rookieYear
            website
            awards{
                season
                eventCode
                teamNumber
                divisionName
                personName
                type
                placement
                team{
                    number
                }
                event{
                    name
                }
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
        await ctx.followup.send(embed=embed)
        return

    team_name = data['data']['teamByNumber']['name']
    school_name = data['data']['teamByNumber']['schoolName']
    sponsors = data['data']['teamByNumber']['sponsors']
    rookie_year = data['data']['teamByNumber']['rookieYear']
    website = data['data']['teamByNumber']['website']


    #Location
    city = data['data']['teamByNumber']['location']['city']
    state = data['data']['teamByNumber']['location']['state']
    country = data['data']['teamByNumber']['location']['country']

    #Awards
    awards = data['data']['teamByNumber']['awards']

    embed = discord.Embed(title="Team: " + str(team_number), description="")

    if team_name:
        embed.add_field(name="Team Name", value=team_name, inline=True)
    if school_name:
        embed.add_field(name="School Name", value=school_name, inline=True)
    if sponsors:
        embed.add_field(name="Sponsors", value=sponsors, inline=True)
    if rookie_year:
        embed.add_field(name="Rookie Year", value=rookie_year, inline=True)
    if website:
        embed.add_field(name="Website", value=website, inline=True)
    if city and state and country:
        embed.add_field(name="Location", value=f"{city}, {state}, {country}", inline=True)

    # Add awards to the embed
    if awards:
        awards_description = ""
        for award in awards:
            awards_description += f"**Season:** {award['season']} \n **Event:** {award['event']['name']} \n **Type:** {award['type']} \n **Placement:** {award['placement']}\n \n"
        if awards_description:
            embed.add_field(name="Awards", value=awards_description, inline=False)

    embed.set_footer(text=universal_footer)

    await ctx.followup.send(embed=embed)

@bot.tree.command(name='seasoninfo', description='Get season statistics for a certain team')
async def season_info(ctx: discord.Interaction, *, team_number: int, season: int):
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
        await ctx.followup.send(embed=embed)
        return
    
    total = data['data']['teamByNumber']['quickStats']['tot']
    autonomous = data['data']['teamByNumber']['quickStats']['auto']
    driver_control = data['data']['teamByNumber']['quickStats']['dc']
    end_game = data['data']['teamByNumber']['quickStats']['eg']
    count = data['data']['teamByNumber']['quickStats']['count']

    embed = discord.Embed(title=f"Season Stats for {team_number}", description=f":calendar_spiral:  Season: {season}", )
    if total:
        embed.add_field(name="Total Score:", value=f":1234: OPR: {round(total['value'], 3)} \n ---------- \n :medal: Rank: {total['rank']}", inline=False)
    if autonomous:
        embed.add_field(name="Auto:", value=f":1234: OPR: {round(autonomous['value'], 3)} \n ---------- \n :medal: Rank: {autonomous['rank']}", inline=True)
    if driver_control:
        embed.add_field(name="TeleOp:", value=f":1234: OPR: {round(driver_control['value'], 3)} \n ---------- \n :medal: Rank: {driver_control['rank']}", inline=True)
    if end_game:
        embed.add_field(name="End Game:", value=f":1234: OPR: {round(end_game['value'], 3)} \n ---------- \n :medal: Rank: {end_game['rank']}", inline=True)

    embed.set_footer(text=universal_footer)

    if count:
        embed.add_field(name=f"Count:", value=f"Rank is out {count} teams", inline=False)

    await ctx.followup.send(embed=embed)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}!')

bot.run(DISCORD_TOKEN, reconnect=True)