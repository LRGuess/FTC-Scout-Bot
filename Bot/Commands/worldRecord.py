import discord
import requests
import os
from dotenv import load_dotenv
from Pages.paginator import Paginator

load_dotenv()
URL = os.getenv('URL')
universal_footer = os.getenv('UNI_FOOTER')

async def world_record(ctx: discord.Interaction, season: int = 2024):
    await ctx.response.defer()

    query = '''
    query worldRecord {
        tradWorldRecord(season: 2024) {
            tournamentLevel
            description
            event {
                name
                code
                location {
                    venue
                    city
                    state
                    country
                }
                start
                end
                timezone
            }
            teams {
                alliance
                team {
                    name
                    number
                }
            }
            scores {
                __typename ... on MatchScores2024 {
                    red {
                        totalPoints
                        totalPointsNp
                        autoPoints
                        dcPoints
                        autoSampleNet
                        autoSampleLow
                        autoSampleHigh
                        autoSpecimenLow
                        autoSpecimenHigh
                        dcSampleNet
                        dcSampleLow
                        dcSampleHigh
                        dcSpecimenLow
                        dcSpecimenHigh
                        minorsCommitted
                        majorsCommitted
                        autoParkPoints
                        autoSamplePoints
                        autoSpecimenPoints
                        dcParkPoints
                        dcSamplePoints
                        dcSpecimenPoints
                    }
                    blue {
                        totalPoints
                        totalPointsNp
                        autoPoints
                        dcPoints
                        autoSampleNet
                        autoSampleLow
                        autoSampleHigh
                        autoSpecimenLow
                        autoSpecimenHigh
                        dcSampleNet
                        dcSampleLow
                        dcSampleHigh
                        dcSpecimenLow
                        dcSpecimenHigh
                        minorsCommitted
                        majorsCommitted
                        autoParkPoints
                        autoSamplePoints
                        autoSpecimenPoints
                        dcParkPoints
                        dcSamplePoints
                        dcSpecimenPoints
                    }
                }
            }
        }
    }
    '''

    response = requests.post(URL, json={'query': query})
    data = response.json()

    world_record = data['data']['tradWorldRecord']
    event = world_record['event']
    teams = world_record['teams']
    tournament_level = world_record['tournamentLevel']
    description = world_record['description']
    name = event['name']
    event_code = event['code']
    location = event['location']
    start = event['start']
    end = event['end']
    timezone = event['timezone']
    red = world_record['scores']['red']
    blue = world_record['scores']['blue']

    embeds = []
    embed = discord.Embed(title=f"World Record", description=f":calendar_spiral: Season: {season}", color=0x00ff00)
    if name:
        embed.add_field(name="Event Name", value=name, inline=True)
    if event_code:
        embed.add_field(name="Event code", value=event_code, inline=True)
    if tournament_level:
        embed.add_field(name="Tournament Level", value=tournament_level, inline=True)
    if description:
        embed.add_field(name="Description", value=description, inline=False)
    if location:    
        embed.add_field(name=":round_pushpin: Location", value=f"{location['venue']}, {location['city']}, {location['state']}, {location['country']}", inline=False)
    if start:
        embed.add_field(name=":clock10: Start Date", value=start, inline=True)
    if end:
        embed.add_field(name=":clock230: End Date", value=end, inline=True)
    if timezone:
        embed.add_field(name=":clock: Timezone", value=timezone, inline=True)
    
    embed.set_footer(text=universal_footer)

    embeds.append(embed)

    embed2 = discord.Embed(title=f"World Record", description=f":calendar_spiral: Season: {season}", color=0x00ff00)
    if red and blue:
        if red['totalPoints']:
            embed2.add_field(name="Red Alliance", value=f"Total Points: {red['totalPoints']} \n \n **Auto** \n **-------** \n Total: {red['autoPoints']} \n ------- \n *Samples:* \n ------- \n Net Zone: {red['autoSampleNet']} \n Low Basket: {red['autoSampleLow']} \n High Basket: {red['autoSampleHigh']} \n Total Sample: {red['autoSamplePoints']} \n ------- \n *Specimens* \n ------- \n Low Bar: {red['autoSpecimenLow']} \n High Bar: {red['autoSpecimenHigh']} \n Total Specimen Points {red['autoSpecimenPoints']} \n ------- \n *Park* \n ------- \n Park Points: {red['autoParkPoints']} \n **-------** \n **Drive Controlled** \n **-------** \n *Samples* \n ------- \n Net Zone: {red['dcSampleNet']} \n Low Basket: {red['dcSampleLow']} \n High Basket {red['dcSampleHigh']} \n Total Sample: {red['dcSamplePoints']} \n ------- \n *Specimens* \n ------- \n Low Bar: {red['dcSpecimenLow']} \n High Bar: {red['dcSpecimenHigh']} \n Total Specimen: {red['dcSpecimenPoints']} \n ------- \n *Park* \n ------- \n Park Points: {red['dcParkPoints']} \n **-------** \n *Penalties* \n **-------** \n Majors: {red['majorsCommitted']} \n Minors: {red['minorsCommitted']} \n Total Without Penalties: {red['totalPointsNp']}", inline=True)
        if blue['totalPoints']:
            embed2.add_field(name="Blue Alliance", value=f"Total Points: {blue['totalPoints']} \n \n **Auto** \n **-------** \n Total: {blue['autoPoints']} \n ------- \n *Samples:* \n ------- \n Net Zone: {blue['autoSampleNet']} \n Low Basket: {blue['autoSampleLow']} \n High Basket: {blue['autoSampleHigh']} \n Total Sample: {blue['autoSamplePoints']} \n ------- \n *Specimens* \n ------- \n Low Bar: {blue['autoSpecimenLow']} \n High Bar: {blue['autoSpecimenHigh']} \n Total Specimen Points {blue['autoSpecimenPoints']} \n ------- \n *Park* \n ------- \n Park Points: {blue['autoParkPoints']} \n **-------** \n **Drive Controlled** \n **-------** \n *Samples* \n ------- \n Net Zone: {blue['dcSampleNet']} \n Low Basket: {blue['dcSampleLow']} \n High Basket {blue['dcSampleHigh']} \n Total Sample: {blue['dcSamplePoints']} \n ------- \n *Specimens* \n ------- \n Low Bar: {blue['dcSpecimenLow']} \n High Bar: {blue['dcSpecimenHigh']} \n Total Specimen: {blue['dcSpecimenPoints']} \n ------- \n *Park* \n ------- \n Park Points: {blue['dcParkPoints']} \n **-------** \n *Penalties* \n **-------** \n Majors: {blue['majorsCommitted']} \n Minors: {blue['minorsCommitted']} \n Total Without Penalties: {blue['totalPointsNp']}", inline=True)        

    embed2.set_footer(text=universal_footer)

    embeds.append(embed2)

    if teams:
        team_description = ""
        for team in teams:
            team_info = f"**Team #:** {team['team']['number']} \n **Team Name:** {team['team']['name']} \n **Alliance:** {team['alliance']} \n"
            team_info += "\n"
            if len(team_description) + len(team_info) > 1024:
                embed = discord.Embed(title=f"Event: {name}", description=f":calendar_spiral: Season: {season}", color=0x00ff00)
                embed.add_field(name="Teams", value=team_description, inline=False)
                embed.set_footer(text=universal_footer)
                embeds.append(embed)
                team_description = team_info
            else:
                team_description += team_info
        if team_description:
            embed = discord.Embed(title=f"Event: {name}", description=f":calendar_spiral: Season: {season}", color=0x00ff00)
            embed.add_field(name="Teams", value=team_description, inline=False)
            embed.set_footer(text=universal_footer)
            embeds.append(embed)

    if embeds:
        view = Paginator(embeds)
        await ctx.followup.send(embed=embeds[0], view=view)