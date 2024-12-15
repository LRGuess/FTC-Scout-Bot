import discord
import requests
import os
from dotenv import load_dotenv
from Pages.paginator import Paginator

load_dotenv()
URL = os.getenv('URL')
universal_footer = os.getenv('UNI_FOOTER')

async def event_search(ctx: discord.Interaction, *, event_name: str, limit: int = 50, season: int = 2024):
    await ctx.response.defer()

    query = '''
    query eventsSearch {
        eventsSearch(searchText: "''' + event_name + '''", limit: ''' + str(limit) +''', season: ''' + str(season) + ''') {
            name
            code
            start
            end
            location{
                venue
                city
                state
                country
            }
            regionCode
        }
    }
    '''

    response = requests.post(URL, json={'query': query})
    data = response.json()

    try:
        events = data['data']['eventsSearch']
    except:
        events = None

    if events == None:
        embed = discord.Embed(title=f"Event {event_name} found", description="Please enter a valid event name", color=0xfc585b)
        await ctx.followup.send(embed=embed)
        return

    embeds = []
    if events:
        event_description = ""
        for event in events:
            event_info = f"**Event Name:** {event['name']} \n **Event Code:** {event['code']} \n **Start Date:** {event['start']} \n **End Date:** {event['end']} \n"
            location = event.get('location')
            if location:
                venue = location.get('venue')
                city = location.get('city')
                state = location.get('state')
                country = location.get('country')
                if venue and city and state and country:
                    event_info += f"**Location:** {venue}, {city}, {state}, {country} \n"
            event_info += "\n"
            if len(event_description) + len(event_info) > 1024:
                embed = discord.Embed(title=f"Events with the name: {event_name}", description=f"Season: {season}", color=0x00ff00)
                embed.add_field(name="Events", value=event_description, inline=False)
                embed.set_footer(text=universal_footer)
                embeds.append(embed)
                event_description = event_info
            else:
                event_description += event_info
        if event_description:
            embed = discord.Embed(title=f"Events with the name: {event_name}", description=f"Season: {season}", color=0x00ff00)
            embed.add_field(name="Events", value=event_description, inline=False)
            embed.set_footer(text=universal_footer)
            embeds.append(embed)
    if embeds:
        view = Paginator(embeds)
        await ctx.followup.send(embed=embeds[0], view=view)
    else:
        embed = discord.Embed(title=f"Events with the name: {event_name}", description="No events found.", color=0xff0000)
        embed.set_footer(text=universal_footer)
        await ctx.followup.send(embed=embed)