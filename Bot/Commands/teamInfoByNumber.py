import discord
import requests
import os
from dotenv import load_dotenv
from Pages.paginator import Paginator

load_dotenv()
URL = os.getenv('URL')
universal_footer = os.getenv('UNI_FOOTER')

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
        embed.set_footer(text=universal_footer)
        await ctx.followup.send(embed=embed)
        return

    team_name = data['data']['teamByNumber']['name']
    school_name = data['data']['teamByNumber']['schoolName']
    sponsors = data['data']['teamByNumber']['sponsors']
    rookie_year = data['data']['teamByNumber']['rookieYear']
    website = data['data']['teamByNumber']['website']

    # Location
    city = data['data']['teamByNumber']['location']['city']
    state = data['data']['teamByNumber']['location']['state']
    country = data['data']['teamByNumber']['location']['country']

    # Awards
    awards = data['data']['teamByNumber']['awards']

    embeds = []
    embed = discord.Embed(title="Team: " + str(team_number), description="")

    if team_name:
        embed.add_field(name="Team Name", value=team_name, inline=True)
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
                embed = discord.Embed(title="Team: " + str(team_number), description="")
                embed.add_field(name="Awards", value=awards_description, inline=False)
                embed.set_footer(text=universal_footer)
                embeds.append(embed)
                awards_description = award_info
            else:
                awards_description += award_info
        if awards_description:
            embed = discord.Embed(title="Team: " + str(team_number), description="")
            embed.add_field(name="Awards", value=awards_description, inline=False)
            embed.set_footer(text=universal_footer)
            embeds.append(embed)

    if embeds:
        view = Paginator(embeds)
        await ctx.followup.send(embed=embeds[0], view=view)
    else:
        embed = discord.Embed(title="Team: " + str(team_number), description="No awards found.", color=0xff0000)
        embed.set_footer(text=universal_footer)
        await ctx.followup.send(embed=embed)