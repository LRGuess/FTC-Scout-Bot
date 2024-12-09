import discord
from discord.ext import commands
from discord.ui import View, Button
import requests
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
URL = 'https://api.ftcscout.org/graphql'

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

universal_footer = "Made with ♥ by Liam from 22212, FTC Scout API"

class Paginator(View):
    def __init__(self, embeds):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.current_page = 0
        self.update_buttons()

    def update_buttons(self):
        self.first_page.disabled = self.current_page == 0
        self.previous_page.disabled = self.current_page == 0
        self.next_page.disabled = self.current_page == len(self.embeds) - 1
        self.last_page.disabled = self.current_page == len(self.embeds) - 1
        self.page_indicator.label = f"Page {self.current_page + 1}/{len(self.embeds)}"

    @discord.ui.button(label="First", style=discord.ButtonStyle.primary)
    async def first_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page = 0
            self.update_buttons()
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    @discord.ui.button(label="Page 1/1", style=discord.ButtonStyle.secondary, disabled=True)
    async def page_indicator(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.embeds) - 1:
            self.current_page += 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    @discord.ui.button(label="Last", style=discord.ButtonStyle.primary)
    async def last_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.embeds) - 1:
            self.current_page = len(self.embeds) - 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

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

@bot.tree.command(name='seasoninfo', description='Get season statistics for a certain team')
async def season_info(ctx: discord.Interaction, *, team_number: int, season: int = 2024):
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
    
    quickStats = data['data']['teamByNumber']['quickStats']
    if quickStats:
        total = quickStats['tot']
        autonomous = quickStats['auto']
        driver_control = quickStats['dc']
        end_game = quickStats['eg']
        count = quickStats['count']

        embed = discord.Embed(title=f"Season Stats for {team_number}", description=f":calendar_spiral:  Season: {season}", )
        if total:
            embed.add_field(name="Total Score:", value=f":1234: OPR: {round(total['value'], 3)} \n ---------- \n :medal: Rank: {total['rank']}", inline=False)
        if autonomous:
            embed.add_field(name="Auto:", value=f":1234: OPR: {round(autonomous['value'], 3)} \n ---------- \n :medal: Rank: {autonomous['rank']}", inline=True)
        if driver_control:
            embed.add_field(name="TeleOp:", value=f":1234: OPR: {round(driver_control['value'], 3)} \n ---------- \n :medal: Rank: {driver_control['rank']}", inline=True)
        if end_game:
            embed.add_field(name="End Game:", value=f":1234: OPR: {round(end_game['value'], 3)} \n ---------- \n :medal: Rank: {end_game['rank']}", inline=True)

        if count:
            embed.add_field(name=f"Count:", value=f"Rank is out {count} teams", inline=False)
    else:
        embed = discord.Embed(title=f"Season Stats for {team_number}", description=f"No quick stats available for season {season}", color=0xfc585b)

    embed.set_footer(text=universal_footer)

    await ctx.followup.send(embed=embed)

@bot.tree.command(name="teamsearch", description="Search for a team by name")
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

@bot.tree.command(name="eventsearch", description="Search for an event by name")
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

    events = data['data']['eventsSearch']

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

@bot.tree.command(name="eventinfo", description="Get information about an event")
async def event_info(ctx: discord.Interaction, *, event_code: str, season: int = 2024, show_teams: bool = False, show_matches: bool = False, show_awards: bool = False):
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
            teams{
            team{
                number
                name
            }
            }
            awards{
            type
            placement
            team{
            name
            number
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
    teams = event['teams']
    awards = event['awards']
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

    embeds.append(embed)

    if matches and show_matches:
        match_description = ""
        for match in matches:
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
        if match_description:
            embed = discord.Embed(title=f"Event: {name}", description=f":calendar_spiral: Season: {season}", color=0x00ff00)
            embed.add_field(name="Matches \n", value=match_description, inline=False)
            embed.set_footer(text=universal_footer)
            embeds.append(embed)

    if teams and show_teams:
        team_description = ""
        for team in teams:
            team_info = f"**Team #:** {team['team']['number']} \n **Team Name:** {team['team']['name']} \n"
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

    if awards and show_awards:
        awards_description = ""
        for award in awards:
            award_info = f"**Type:** {award['type']} \n **Placement:** {award['placement']} \n **Team Name:** {award['team']['name']} \n **Team #:** {award['team']['number']} \n"
            award_info += "\n"
            if len(awards_description) + len(award_info) > 1024:
                embed = discord.Embed(title=f"Event: {name}", description=f":calendar_spiral: Season: {season}", color=0x00ff00)
                embed.add_field(name="Awards", value=awards_description, inline=False)
                embed.set_footer(text=universal_footer)
                embeds.append(embed)
                awards_description = award_info
            else:
                awards_description += award_info
        if awards_description:
            embed = discord.Embed(title=f"Event: {name}", description=f":calendar_spiral: Season: {season}", color=0x00ff00)
            embed.add_field(name="Awards", value=awards_description, inline=False)
            embed.set_footer(text=universal_footer)
            embeds.append(embed)

    if embeds:
        view = Paginator(embeds)
        await ctx.followup.send(embed=embeds[0], view=view)
    else:
        embed = discord.Embed(title=f"Event: {name}", description="No matches found.", color=0xff0000)
        embed.set_footer(text=universal_footer)
        await ctx.followup.send(embed=embed) 

@bot.tree.command(name="worldrecord", description="Get the world record for a certain season")
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

    embeds.append(embed)

    embed2 = discord.Embed(title=f"World Record", description=f":calendar_spiral: Season: {season}", color=0x00ff00)
    if red and blue:
        if red['totalPoints']:
            embed2.add_field(name="Red Alliance", value=f"Total Points: {red['totalPoints']} \n \n **Auto** \n **-------** \n Total: {red['autoPoints']} \n ------- \n *Samples:* \n ------- \n Net Zone: {red['autoSampleNet']} \n Low Basket: {red['autoSampleLow']} \n High Basket: {red['autoSampleHigh']} \n Total Sample: {red['autoSamplePoints']} \n ------- \n *Specimens* \n ------- \n Low Bar: {red['autoSpecimenLow']} \n High Bar: {red['autoSpecimenHigh']} \n Total Specimen Points {red['autoSpecimenPoints']} \n ------- \n *Park* \n ------- \n Park Points: {red['autoParkPoints']} \n **-------** \n **Drive Controlled** \n **-------** \n *Samples* \n ------- \n Net Zone: {red['dcSampleNet']} \n Low Basket: {red['dcSampleLow']} \n High Basket {red['dcSampleHigh']} \n Total Sample: {red['dcSamplePoints']} \n ------- \n *Specimens* \n ------- \n Low Bar: {red['dcSpecimenLow']} \n High Bar: {red['dcSpecimenHigh']} \n Total Specimen: {red['dcSpecimenPoints']} \n ------- \n *Park* \n ------- \n Park Points: {red['dcParkPoints']} \n **-------** \n *Penalties* \n **-------** \n Majors: {red['majorsCommitted']} \n Minors: {red['minorsCommitted']} \n Total Without Penalties: {red['totalPointsNp']}", inline=True)
        if blue['totalPoints']:
            embed2.add_field(name="Blue Alliance", value=f"Total Points: {blue['totalPoints']} \n \n **Auto** \n **-------** \n Total: {blue['autoPoints']} \n ------- \n *Samples:* \n ------- \n Net Zone: {blue['autoSampleNet']} \n Low Basket: {blue['autoSampleLow']} \n High Basket: {blue['autoSampleHigh']} \n Total Sample: {blue['autoSamplePoints']} \n ------- \n *Specimens* \n ------- \n Low Bar: {blue['autoSpecimenLow']} \n High Bar: {blue['autoSpecimenHigh']} \n Total Specimen Points {blue['autoSpecimenPoints']} \n ------- \n *Park* \n ------- \n Park Points: {blue['autoParkPoints']} \n **-------** \n **Drive Controlled** \n **-------** \n *Samples* \n ------- \n Net Zone: {blue['dcSampleNet']} \n Low Basket: {blue['dcSampleLow']} \n High Basket {blue['dcSampleHigh']} \n Total Sample: {blue['dcSamplePoints']} \n ------- \n *Specimens* \n ------- \n Low Bar: {blue['dcSpecimenLow']} \n High Bar: {blue['dcSpecimenHigh']} \n Total Specimen: {blue['dcSpecimenPoints']} \n ------- \n *Park* \n ------- \n Park Points: {blue['dcParkPoints']} \n **-------** \n *Penalties* \n **-------** \n Majors: {blue['majorsCommitted']} \n Minors: {blue['minorsCommitted']} \n Total Without Penalties: {blue['totalPointsNp']}", inline=True)        

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


@bot.tree.command(name="gamemanual", description="Get a link to the game manual")
async def game_manual(ctx: discord.Interaction):
    await ctx.response.defer()

    embed = discord.Embed(title="Game Manual", description="Here is the link to the game manual", color=0xf57f26)
    embed.add_field(name="Game Manual", value="[Game Manual](https://ftc-resources.firstinspires.org/file/ftc/game/manual)", inline=False)

    await ctx.followup.send(embed=embed)

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