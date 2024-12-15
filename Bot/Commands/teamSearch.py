import discord
import requests
import os
from dotenv import load_dotenv
from Pages.paginator import Paginator

load_dotenv()
URL = os.getenv('URL')
universal_footer = os.getenv('UNI_FOOTER')

async def team_search(ctx: discord.Interaction, *, team_name: str, limit: int = 50, season: int = 2024):
    await ctx.response.defer()
    query = '''
    query teamSearch {
        teamsSearch(searchText: "''' + team_name + '''", limit: ''' + str(limit) +''') {
            number
            name
            quickStats(season: ''' + str(season) + ''') {
                tot{value, rank}
            }
        }  
    }
    '''

    response = requests.post(URL, json={'query': query})
    data = response.json()

    teams = data['data']['teamsSearch']

    embeds = []
    if teams:
        teams_description = ""
        for team in teams:
            team_info = f"**Team #:** {team['number']} \n **Team Name:** {team['name']} \n"
            quickStats = team.get('quickStats')
            if quickStats:
                total = quickStats.get('tot')
                if total:
                    team_info += f"**Total OPR:** {round(total['value'], 3)} \n **Overall Rank:** {total['rank']} \n"
            team_info += "\n"
            if len(teams_description) + len(team_info) > 1024:
                embed = discord.Embed(title=f"Teams with the name: {team_name}", description=f"Season: {season}", color=0x00ff00)
                embed.add_field(name="Teams", value=teams_description, inline=False)
                embed.set_footer(text=universal_footer)
                embeds.append(embed)
                teams_description = team_info
            else:
                teams_description += team_info
        if teams_description:
            embed = discord.Embed(title=f"Teams with the name: {team_name}", description=f"Season: {season}", color=0x00ff00)
            embed.add_field(name="Teams", value=teams_description, inline=False)
            embed.set_footer(text=universal_footer)
            embeds.append(embed)

    if embeds:
        view = Paginator(embeds)
        await ctx.followup.send(embed=embeds[0], view=view)
    else:
        embed = discord.Embed(title=f"Teams with the name: {team_name}", description="No teams found.", color=0xff0000)
        embed.set_footer(text=universal_footer)
        await ctx.followup.send(embed=embed)