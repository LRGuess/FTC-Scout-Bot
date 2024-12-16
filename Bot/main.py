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
import Commands.about as about_text
import Commands.help as help_text

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

@bot.tree.command(name="matchesplayed", description="How many matches have been played until now!")
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
    await about_text.about(ctx)

@bot.tree.command(name="help", description="Get help with the bot")
async def help(ctx: discord.Interaction):
    await help_text.help(ctx)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}!')

bot.run(DISCORD_TOKEN, reconnect=True)