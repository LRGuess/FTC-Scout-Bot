import discord
import requests
import os
from dotenv import load_dotenv
from Pages.paginator import Paginator

load_dotenv()
URL = os.getenv('URL')
universal_footer = os.getenv('UNI_FOOTER')

async def match_info(ctx: discord.Interaction, *, event_code: str, match_id: int , season: int = 2024):
    await ctx.response.defer()

    query = '''
        query eventByCode {
            eventByCode(season: ''' + str(season) + ''', code: "''' + str(event_code) + '''") {
                name
                type
                location{
                    venue
                    state
                    city
                    country
                }
                start
                end
                timezone
                liveStreamURL
                matches{
                    description
                    id
                    scores{
                        __typename ... on MatchScores2024{
                            red{totalPoints, autoPoints, dcPoints}
                            blue{totalPoints, autoPoints, dcPoints}
                        }    
                    }
                }
            }
        }
    '''

    response = requests.post(URL, json={'query': query})
    data = response.json()

    event = data['data']['eventByCode']
    name = event['name']
    event_type = event['type']
    start = event['start']
    end = event['end']
    location = event['location']
    venue = location['venue']
    city = location['city']
    state = location['state']
    country = location['country']
    matches = event['matches']
    live_stream_url = event.get('liveStreamURL')
    timezone = event['timezone']

    embeds = []
    embed = discord.Embed(title=f"Event: {name}", description=f":calendar_spiral: Season: {season}", color=0x00ff00)
    if event_type:
        embed.add_field(name=":label: Type", value=event_type, inline=False)
    if live_stream_url:
        embed.add_field(name=":tv: Live Stream", value=live_stream_url, inline=False)
    if location:    
        embed.add_field(name=":round_pushpin: Location", value=f"{venue}, {city}, {state}, {country}", inline=True)
    if start:
        embed.add_field(name=":clock10: Start Date", value=start, inline=False)
    if end:
        embed.add_field(name=":clock230: End Date", value=end, inline=False)
    if timezone:
        embed.add_field(name=":clock: Timezone", value=timezone, inline=False)

    embed.set_footer(text=universal_footer)

    embeds.append(embed)

    if matches:
        match_description = ""
        for match in matches:
            if match['id'] == match_id:
                match_info = f"**Match ID:** {match['id']}, {match['description']} \n"
                scores = match.get('scores')
                if scores:
                    red = scores.get('red')
                    blue = scores.get('blue')
                    if red and blue:
                        match_info += f"-------------- \n"
                        match_info += f"**Red - Blue** \n"
                        match_info += f"Total: {red['totalPoints']} / {blue['totalPoints']} \n"
                        match_info += f"Auto: {red['autoPoints']} / {blue['autoPoints']} \n"
                        match_info += f"TeleOp: {red['dcPoints']} / {blue['dcPoints']} \n"
                match_info += "\n"
                if len(match_description) + len(match_info) > 1024:
                    embed = discord.Embed(title=f"Event: {name}", description=f":calendar_spiral: Season: {season}", color=0x00ff00)
                    embed.add_field(name="Matches \n", value=match_description, inline=False)
                    embed.set_footer(text=universal_footer)
                    embeds.append(embed)
                    match_description = match_info
                else:
                    match_description += match_info
            else:
                embed = discord.Embed(title=f"Match not found", description=f"No match with match id {match_id} found in event {event_code}", color=0xff0000)
                embed.set_footer(text=universal_footer)
                await ctx.followup.send(embed=embed)
        if match_description:
            embed = discord.Embed(title=f"Event: {name}", description=f":calendar_spiral: Season: {season}", color=0x00ff00)
            embed.add_field(name="Matches \n", value=match_description, inline=False)
            embed.set_footer(text=universal_footer)
            embeds.append(embed)

    if embeds:
        view = Paginator(embeds)
        await ctx.followup.send(embed=embeds[0], view=view)
    else:
        embed = discord.Embed(title=f"Event: {name}", description="No matches found.", color=0xff0000)
        embed.set_footer(text=universal_footer)
        await ctx.followup.send(embed=embed)