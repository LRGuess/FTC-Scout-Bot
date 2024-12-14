import discord
import requests
import os
from dotenv import load_dotenv
from Pages.paginator import Paginator

load_dotenv()
URL = os.getenv('URL')
universal_footer = os.getenv('UNI_FOOTER')

async def team_info_by_name(ctx: discord.Interaction, *, team_name: str):
    await ctx.response.defer()

    query = '''
    query teamByName {
        teamByName(name: "''' + str(team_name) +'''") {
            name
            number
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
        teamByName = data['data']['teamByName']
    except:
        teamByName = None
    
    if teamByName == None:
        embed = discord.Embed(title="Team name not found", description="Please enter a valid team name, or use /teamsearch", color=0xfc585b)
        embed.set_footer(text=universal_footer)
        await ctx.followup.send(embed=embed)
        return

    team_name = data['data']['teamByName']['name']
    team_number = data['data']['teamByName']['number']
    school_name = data['data']['teamByName']['schoolName']
    sponsors = data['data']['teamByName']['sponsors']
    rookie_year = data['data']['teamByName']['rookieYear']
    website = data['data']['teamByName']['website']

    # Location
    city = data['data']['teamByName']['location']['city']
    state = data['data']['teamByName']['location']['state']
    country = data['data']['teamByName']['location']['country']

    # Awards
    awards = data['data']['teamByName']['awards']

    embeds = []
    embed = discord.Embed(title="Team: " + str(team_name), description="")

    if team_name:
        embed.add_field(name="Team Number", value=team_number, inline=True)
    if school_name:
        embed.add_field(name=":school: School Name", value=school_name, inline=True)
    if sponsors:
        embed.add_field(name=":money_with_wings: Sponsors", value=sponsors, inline=True)
    if rookie_year:
        embed.add_field(name=":date: Rookie Year", value=rookie_year, inline=True)
    if website:
        embed.add_field(name=":globe_with_meridians: Website", value=website, inline=True)
    if city and state and country:
        embed.add_field(name=":round_pushpin: Location", value=f"{city}, {state}, {country}", inline=True)

    embeds.append(embed)

    # Add awards to the embed
    if awards:
        awards_description = ""
        for award in awards:
            award_info = f"**:calendar_spiral: Season:** {award['season']} \n **:round_pushpin: Event:** {award['event']['name']} \n **:receipt: Type:** {award['type']} \n **:military_medal: Placement:** {award['placement']}\n \n"
            if len(awards_description) + len(award_info) > 1024:
                embed = discord.Embed(title="Team: " + str(team_name), description="")
                embed.add_field(name="Awards", value=awards_description, inline=False)
                embed.set_footer(text=universal_footer)
                embeds.append(embed)
                awards_description = award_info
            else:
                awards_description += award_info
        if awards_description:
            embed = discord.Embed(title="Team: " + str(team_name), description="")
            embed.add_field(name="Awards", value=awards_description, inline=False)
            embed.set_footer(text=universal_footer)
            embeds.append(embed)

    if embeds:
        view = Paginator(embeds)
        await ctx.followup.send(embed=embeds[0], view=view)
    else:
        embed = discord.Embed(title="Team: " + str(team_name), description="No awards found.", color=0xff0000)
        embed.set_footer(text=universal_footer)
        await ctx.followup.send(embed=embed)