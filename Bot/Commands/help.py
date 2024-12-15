import discord
import os
from dotenv import load_dotenv

load_dotenv()
universal_footer = os.getenv('UNI_FOOTER')

async def help(ctx: discord.Interaction):
    await ctx.response.defer()

    embed = discord.Embed(title="Help", description="Here are the commands you can use with the bot. \n Anything with an * is required \n Any anspecified season will default to the current one", color=0x00ff00)
    embed.add_field(name="/teaminfo <team_number>*", value="Get general information about a team", inline=False)
    embed.add_field(name="/seasoninfo <team_number>* <season>", value="Get season statistics for a team", inline=False)
    embed.add_field(name="/teamsearch <team_name>* <limit> <season>", value="Search for a team by name. Limit limits the amount of results shown", inline=False)
    embed.add_field(name="/eventsearch <event_name>* <limit> <season>", value="Search for an event by name. Limit limits the amount of results shown", inline=False)
    embed.add_field(name="/eventinfo <event_code>* <season> <show_teams> <show_matches> <show_awards>", value="Get information about an event. If show_matches is True, the embed will display info for all matches. If show_teams is True, embed will show all teams. If show_awards is True, embed will show the awards granted.", inline=False)
    embed.add_field(name="/gamemanual", value="Get a link to the game manual", inline=False)
    embed.add_field(name="/about", value="Get information about the bot", inline=False)
    embed.add_field(name="/help", value="Get help with the bot", inline=False)

    embed.set_footer(text=universal_footer)

    await ctx.followup.send(embed=embed)