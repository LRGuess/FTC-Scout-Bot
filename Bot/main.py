import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import Commands.teamInfoByNumber as teamInfoByNumber
import Commands.teamInfoByName as teamInfoByName
import Commands.seasonInfo as seasonInfo
import Commands.teamSearch as teamSearch
import Commands.eventSearch as eventSearch
import Commands.eventInfo as eventInfo
import Commands.worldRecord as worldRecord
import Commands.matchesPlayed as matchesPlayed
import Commands.inspectRobot as inspect
import Commands.gameManual as gameManual

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
URL = os.getenv('URL')

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

universal_footer = os.getenv('UNI_FOOTER')

@bot.tree.command(name='teaminfo', description='Generalized team info')
async def team_info_by_number(ctx: discord.Interaction, *, team_number: int):
    await teamInfoByNumber.team_info_by_number(ctx, team_number=team_number)

@bot.tree.command(name='teaminfobyname', description='Generalized team info')
async def team_info_by_name(ctx: discord.Interaction, *, team_name: str):
    await teamInfoByName.team_info_by_name(ctx, team_name=team_name)

@bot.tree.command(name='seasoninfo', description='Get season statistics for a certain team')
async def season_info(ctx: discord.Interaction, *, team_number: int, season: int = 2024):
    await seasonInfo.season_info(ctx, team_number=team_number, season=season)

@bot.tree.command(name="teamsearch", description="Search for a team by name")
async def team_search(ctx: discord.Interaction, *, team_name: str, limit: int = 50, season: int = 2024):
    await teamSearch.team_search(ctx, team_name=team_name, limit=limit, season=season)

@bot.tree.command(name="eventsearch", description="Search for an event by name")
async def event_search(ctx: discord.Interaction, *, event_name: str, limit: int = 50, season: int = 2024):
    await eventSearch.event_search(ctx, event_name=event_name, limit=limit, season=season)

@bot.tree.command(name="eventinfo", description="Get information about an event")
async def event_info(ctx: discord.Interaction, *, event_code: str, season: int = 2024, show_teams: bool = False, show_matches: bool = False, show_awards: bool = False):
    await eventInfo.event_info(ctx, event_code=event_code, season=season, show_teams=show_teams, show_matches=show_matches, show_awards=show_awards)

@bot.tree.command(name="worldrecord", description="Get the world record for a certain season")
async def world_record(ctx: discord.Interaction, season: int = 2024):
    await worldRecord.world_record(ctx, season=season)

@bot.tree.command(name="matchplayed", description="How many matches have been played until now!")
async def matches_played(ctx: discord.Interaction, season: int = 2024):
    await matchesPlayed.matches_played(ctx, season=season)

@bot.tree.command(name="inspect", description="Runs Robot Inspection")
async def robot_inspection(ctx: discord.Interaction):
    await inspect.robot_inspection(ctx)

@bot.tree.command(name="gamemanual", description="Get a link to the game manual")
async def game_manual(ctx: discord.Interaction):
    await gameManual.game_manual(ctx)

@bot.tree.command(name='about', description='Get information about the bot')
async def about(ctx: discord.Interaction):
    await ctx.response.defer()

    embed = discord.Embed(title="About", description="This bot is a Discord bot that uses the FTC Scout API to get information about teams and their statistics", color=0x00ff00)
    embed.add_field(name="Author", value="Liam Ramirez-Guess from 22212", inline=False)
    embed.add_field(name="Support Server", value="https://discord.gg/D4WUX7r3", inline=False)
    embed.add_field(name="FTC Scout", value="https://ftcscout.org", inline=False)
    embed.add_field(name="Version", value="1.0", inline=False)

    await ctx.followup.send(embed=embed)

@bot.tree.command(name="help", description="Get help with the bot")
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

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}!')

bot.run(DISCORD_TOKEN, reconnect=True)