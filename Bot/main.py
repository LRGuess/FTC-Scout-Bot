import discord
from discord.ext import commands
from discord.ui import View, Button
import requests
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
import Pages.paginator as Paginator

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
URL = os.getenv('URL')

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

universal_footer = os.getenv('UNI_FOOTER')

class Inspector(View):
    def __init__(self, embeds):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.current_page = 0
        self.update_buttons()

    def update_buttons(self):
        self.next_page.disabled = self.current_page == len(self.embeds) - 1
        self.fail.disabled = self.current_page == len(self.embeds) - 1 or self.current_page == 0

    @discord.ui.button(label="✅", style=discord.ButtonStyle.green)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.embeds) - 1:
            self.current_page += 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    @discord.ui.button(label="❌", style=discord.ButtonStyle.red)
    async def fail(self, interaction: discord.Interaction, button: discord.ui.Button):
        fail_embed = discord.Embed(title="Inspection Failed", description=f"{self.embeds[self.current_page].description} \n Check the corresponding rule! \n {self.embeds[self.current_page].footer.text}", color=0xff0000)
        self.fail.disabled = True
        self.next_page.disabled = True
        await interaction.response.edit_message(embed=fail_embed, view=None)

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
    await ctx.response.defer()

    inspection_footer = "Rule in Game Manual: "

    embeds = []
    cover = discord.Embed(title="Robot / Field Inspection", description="Welcome to Robot inspection! This will simulate at-Comp robot inspection, but please not the in-person inspectors will always have the final say and this is nothing but a tool. Passing this inspection does not mean you are cometition-ready, it just means you are likly to pass as Comp!", color=0x4472c4)
    cover.set_footer(text=universal_footer)
    embeds.append(cover)

    #Robot Size

    I303 = discord.Embed(title="Robot - Size", description="ROBOT is presented at inspection with all MECHANISMS (including all COMPONENTS of each MECHANISM), configurations, and decorations used on the ROBOT. ", color=0x4472c4)
    I303.set_footer(text=inspection_footer + "I303")
    embeds.append(I303)

    R101 = discord.Embed(title="Robot - Size", description="The ROBOT in all of its STARTING CONFIGURATIONS must fit within an 18” cube as it would start the MATCH.", color=0x4472c4)
    R101.set_footer(text=inspection_footer + "R101")
    embeds.append(R101)

    R104 = discord.Embed(title="Robot - Size", description="ROBOT may not expand or reach outside of a 20” x 42” horizontal boundary at any time during the MATCH (may be hardware or software limited).", color=0x4472c4)
    R104.set_footer(text=inspection_footer + "R104")
    embeds.append(R104)

    #Robot Signs
    R401 = discord.Embed(title="Robot - Signs", description="ROBOT has two ROBOT SIGNS that are located on opposite or adjacent sides of the ROBOT and visible to FIELD STAFF from at least 12 feet away and meet minimal size requirements.", color=0x4472c4)
    R401.set_footer(text=inspection_footer + "R401")
    embeds.append(R401)

    R402 = discord.Embed(title="Robot - Signs", description="ROBOT SIGNS can indicate both ALLIANCE colors and meets markings requirements, unpowered.", color=0x4472c4)
    R402.set_footer(text=inspection_footer + "R402")
    embeds.append(R402)

    R403 = discord.Embed(title="Robot - Signs", description="Team number is displayed on ROBOT SIGNS and meets number size requirements, unpowered.", color=0x4472c4)
    R403.set_footer(text=inspection_footer + "R403")
    embeds.append(R403)

    #Robot Mechanical
    R201R202 = discord.Embed(title="Robot - Mechanical", description="ROBOT does not contain any COMPONENTS that could harm people, damage the ARENA, or damage other ROBOTS. This includes sharp edges, protrusions, or hazards to the ARENA elements.", color=0x4472c4)
    R201R202.set_footer(text=inspection_footer + "R201, R202")
    embeds.append(R201R202)

    R203B = discord.Embed(title="Robot - Mechanical", description="ROBOT does not contain devices that generate sound at a level sufficient to be a distraction.", color=0x4472c4)
    R203B.set_footer(text=inspection_footer + "R203.B")
    embeds.append(R203B)

    R203DEGH = discord.Embed(title="Robot - Mechanical", description="ROBOT does not contain materials that are hazardous (i.e., flammable materials/gasses, mercury switches, exposed untreated hazardous materials).", color=0x4472c4)
    R203DEGH.set_footer(text=inspection_footer + "R203.D, E, G, H")
    embeds.append(R203DEGH)

    R205 = discord.Embed(title="Robot - Mechanical", description="ROBOT does not contain materials that would cause a delay of game if released (e.g., coffee beans).", color=0x4472c4)
    R205.set_footer(text=inspection_footer + "R205")
    embeds.append(R205)

    R207 = discord.Embed(title="Robot - Mechanical", description="ROBOT does not contain any closed air or hydraulic devices (i.e., gas springs, compressors, vacuum generating devices). Air-filled pneumatic wheels are exempt from this rule.", color=0x4472c4)
    R207.set_footer(text=inspection_footer + "R207")
    embeds.append(R207)

    R306R307 = discord.Embed(title="Robot - Mechanical", description="ROBOT does not contain prohibited COTS MECHANISMS (multi DoF, game task solving, …). ", color=0x4472c4)
    R306R307.set_footer(text=inspection_footer + "R306, R307")
    embeds.append(R306R307)

    # Robot Electrical
    R503 = discord.Embed(title="Robot - Electrical", description="ROBOT does not contain more than 8 allowed motors and 12 allowed servos.", color=0x4472c4)
    R503.set_footer(text=inspection_footer + "R503")
    embeds.append(R503)

    R504 = discord.Embed(title="Robot - Electrical", description="Actuators are not modified except as explicitly allowed.", color=0x4472c4)
    R504.set_footer(text=inspection_footer + "R504")
    embeds.append(R504)

    R505 = discord.Embed(title="Robot - Electrical", description="Actuators are powered and controlled only from approved devices.", color=0x4472c4)
    R505.set_footer(text=inspection_footer + "R505")
    embeds.append(R505)

    R506 = discord.Embed(title="Robot - Electrical", description="No relays, electromagnets, electrical solenoid actuators, or related systems.", color=0x4472c4)
    R506.set_footer(text=inspection_footer + "R506")
    embeds.append(R506)

    R601R606 = discord.Embed(title="Robot - Electrical", description="Exactly 1 main battery pack of an approved type is on the ROBOT and it is properly connected to the main power switch, securely mounted.", color=0x4472c4)
    R601R606.set_footer(text=inspection_footer + "R601, R606")
    embeds.append(R601R606)

    R609 = discord.Embed(title="Robot - Electrical", description="Exactly 1 approved main power switch must control all power provided by the ROBOT battery pack and must be properly labeled. Secondary switches downstream are allowed if labeled “secondary.”", color=0x4472c4)
    R609.set_footer(text=inspection_footer + "R609")
    embeds.append(R609)

    R602 = discord.Embed(title="Robot - Electrical", description="COTS USB batteries on the ROBOT remain isolated from the ROBOT power systems.", color=0x4472c4)
    R602.set_footer(text=inspection_footer + "R602")
    embeds.append(R602)

    R610R615 = discord.Embed(title="Robot - Electrical", description="Fuses must not be replaced with fuses of higher rating than allowed, no self-resetting fuses allowed.", color=0x4472c4)
    R610R615.set_footer(text=inspection_footer + "R610, R615")
    embeds.append(R610R615)

    R611 = discord.Embed(title="Robot - Electrical", description="If electronics are grounded to the ROBOT frame, the only approved methods are the REV or AndyMark resistive grounding strap and must be connected to a fully COTS XT30 COMPONENT.", color=0x4472c4)
    R611.set_footer(text=inspection_footer + "R611")
    embeds.append(R611)

    R613R618 = discord.Embed(title="Robot - Electrical", description="USTOM CIRCUITS cannot provide >5V regulated power and cannot alter critical power paths. Voltage and current monitoring is okay, as long as the effect is inconsequential.", color=0x4472c4)
    R613R618.set_footer(text=inspection_footer + "R613, R618")
    embeds.append(R613R618)

    R615 = discord.Embed(title="Robot - Electrical", description="Circuits are wired with the appropriately sized insulated copper wire (non-SIGNAL LEVEL wires).", color=0x4472c4)
    R615.set_footer(text=inspection_footer + "R615")
    embeds.append(R615)

    R616 = discord.Embed(title="Robot - Electrical", description="All non-SIGNAL LEVEL wiring is consistently color-coded with different colors used for the positive (red, yellow, white, brown, or black with white stripe) and negative/common (black, blue) wires", color=0x4472c4)
    R616.set_footer(text=inspection_footer + "R616")
    embeds.append(R616)

    R701R704R705R711 = discord.Embed(title="Robot - Electrical", description="The ROBOT must be controlled via 1 ROBOT CONTROLLER (REV Control Hub via USB or RS485, or allowed Android device via USB). The ROBOT CONTROLLER must be visible for inspection.", color=0x4472c4)
    R701R704R705R711.set_footer(text=inspection_footer + "R701, R704, R705, R711")
    embeds.append(R701R704R705R711)

    R714R715 = discord.Embed(title="Robot - Electrical", description="Only allowed USB devices connected to USB (no LEDs, etc.), webcams can only be single-sensor.", color=0x4472c4)
    R714R715.set_footer(text=inspection_footer + "R714, R715")
    embeds.append(R714R715)

    R716 = discord.Embed(title="Robot - Electrical", description="Self-contained video recording devices, if used, must turn off or disable wireless communication.", color=0x4472c4)
    R716.set_footer(text=inspection_footer + "R716")
    embeds.append(R716)

    # FIELD
    # Operator Console

    Field_Cover = discord.Embed(title="Field Inspection", description="You got this far! Time for Field Inspection!", color=0xed7d31)
    Field_Cover.set_footer(text=universal_footer)
    embeds.append(Field_Cover)

    R901 = discord.Embed(title="Field - Operator Console", description="The OPERATOR CONSOLE consists of only of one Android device (Circle): Motorola Moto G4 Play, Motorola Moto G5, Motorola G5 Plus, Motorola Moto E4, Motorola Moto E5, Motorola Moto E5 Play, or REV Driver Hub. If team is not from North America and has an alternate smartphone, circle here.", color=0xed7d31)
    R901.set_footer(text=inspection_footer + "R901")
    embeds.append(R901)

    R902 = discord.Embed(title="Field - Operator Console", description="The touch display screen of the DRIVER STATION device is accessible and visible to FIELD STAFF. ", color=0xed7d31)
    R902.set_footer(text=inspection_footer + "R902")
    embeds.append(R902)

    R903 = discord.Embed(title="Field - Operator Console", description="No more than one (1) optional COTS USB external battery connected to the REV Driver Hub USB-C port, no more than one (1) USB hub connected to the smartphone Android Device. ", color=0xed7d31)
    R903.set_footer(text=inspection_footer + "R903")
    embeds.append(R903)

    R904 = discord.Embed(title="Field - Operator Console", description="The OPERATOR CONSOLE consists of no more than two of the allowed gamepads. ", color=0xed7d31)
    R904.set_footer(text=inspection_footer + "R904")
    embeds.append(R904)

    R905A = discord.Embed(title="Field - Operator Console", description="Does not contain more than 1 external USB hub.", color=0xed7d31)
    R905A.set_footer(text=inspection_footer + "R905.A")
    embeds.append(R905A)

    R905B = discord.Embed(title="Field - Operator Console", description="Does not contain non-decorative electronics not otherwise required.", color=0xed7d31)
    R905B.set_footer(text=inspection_footer + "R905.B")
    embeds.append(R905B)

    R905C = discord.Embed(title="Field - Operator Console", description="Does not exceed 3ft wide, 1ft deep and 2 ft tall (91.4cm by 30.5cm by 61.0 cm) excluding any items that are held or worn by the DRIVE TEAM during a MATCH. ", color=0xed7d31)
    R905C.set_footer(text=inspection_footer + "R905.C")
    embeds.append(R905C)

    # Operator Console and Robot Controller 
    R706 = discord.Embed(title="Field - Operator Console and Robot Controller", description="Communication between the ROBOT CONTROLLER and DRIVER STATION is only through the official RC and DS applications over the ROBOT CONTROLLER Wi-Fi.", color=0xed7d31)
    R706.set_footer(text=inspection_footer + "R706")
    embeds.append(R706)

    R707 = discord.Embed(title="Field - Operator Console and Robot Controller", description="Android smartphone(s), REV Driver Hub, and REV Control Hub are named with the official team number followed by an optional -A (or other letter) and -DS or -RC as appropriate. ", color=0xed7d31)
    R707.set_footer(text=inspection_footer + "R707")
    embeds.append(R707)

    R718BC = discord.Embed(title="Field - Operator Console and Robot Controller", description="Android smartphones (if used) have airplane mode & Wi-Fi enabled, and Bluetooth disabled.", color=0xed7d31)
    R718BC.set_footer(text=inspection_footer + "R718.B, C")
    embeds.append(R718BC)

    R718D = discord.Embed(title="Field - Operator Console and Robot Controller", description="All remembered Wi-Fi Direct Groups and Wi-Fi connections on Android devices (smartphones and REV Driver Hub) have been removed, only ROBOT CONTROLLER Wi-Fi remains.", color=0xed7d31)
    R718D.set_footer(text=inspection_footer + "R718.D")
    embeds.append(R718D)

    R710 = discord.Embed(title="Field - Operator Console and Robot Controller", description="ROBOT CONTROLLER Wi-Fi is set to the correct channel (if required by the competition).", color=0xed7d31)
    R710.set_footer(text=inspection_footer + "R710")
    embeds.append(R710)

    R718AC = discord.Embed(title="Field - Operator Console and Robot Controller", description="REV Control Hub (if used) has Wi-Fi turned on, Bluetooth is turned off, and the password is different than the factory default value of “password” as seen in ROBOT Self-Inspect", color=0xed7d31)
    R718AC.set_footer(text=inspection_footer + "R718.A, C")
    embeds.append(R718AC)

    # Power-On Operation
    NA = discord.Embed(title="Field - Power-On Operation", description="ROBOT CONTROLLER device properly connects with the DRIVER STATION device.", color=0xed7d31)
    NA.set_footer(text=inspection_footer + "N/A")
    embeds.append(NA)

    G401G406 = discord.Embed(title="Field - Power-On Operation", description="ROBOT starts and stops when commanded by the DRIVER STATION device. Specifically, stop button must be able to immediately interrupt both AUTO and TELEOP OpModes.", color=0xed7d31)
    G401G406.set_footer(text=inspection_footer + "G401, G406")
    embeds.append(G401G406)

    # General Notifications and Acknowledgements
    G301 = discord.Embed(title="Field - General Notifications and Acknowledgements", description="Team understands that they must promptly proceed to the ARENA for their scheduled MATCH time as indicated on the MATCH schedule. It is the team’s responsibility to monitor for schedule changes.", color=0xed7d31)
    G301.set_footer(text=inspection_footer + "G301")
    embeds.append(G301)

    G303 = discord.Embed(title="Field - General Notifications and Acknowledgements", description="Team knows that they are responsible for attaching the correct ALLIANCE specific ROBOT SIGN on two sides of their ROBOT before they approach the ARENA.", color=0xed7d31)
    G303.set_footer(text=inspection_footer + "G303")
    embeds.append(G303)

    G414 = discord.Embed(title="Field - General Notifications and Acknowledgements", description="The team understands how to disable their ROBOT, if instructed to do so by a REFEREE.", color=0xed7d31)
    G414.set_footer(text=inspection_footer + "G414")
    embeds.append(G414)

    R706_2 = discord.Embed(title="Field - General Notifications and Acknowledgements", description="Team understands no programming is allowed in the ARENA, including MATCH queue areas.", color=0xed7d31)
    R706_2.set_footer(text=inspection_footer + "R706")
    embeds.append(R706_2)

    R713 = discord.Embed(title="Field - General Notifications and Acknowledgements", description="Team understands that troubleshooting or programming assistance from FIELD STAFF will be limited if team is not using at least the recommended minimum versions of SDK and device software. ", color=0xed7d31)
    R713.set_footer(text=inspection_footer + "R713")
    embeds.append(R713)

    Pass = discord.Embed(title=":tada:", description="Voila! My bot approves yours! Good luck at comp, and follow the real inspector's rules!", color=0x2db567)
    Pass.set_footer(text=universal_footer)
    embeds.append(Pass)

    if embeds:
        view = Inspector(embeds)
        await ctx.followup.send(embed=embeds[0], view=view)
    else:
        embed = discord.Embed(title=f"Something weird happened", description="Please report this error to the [support server]()! **Error code:** IN-53RV3", color=0xcc1532)
        embed.set_footer(text=universal_footer)
        await ctx.followup.send(embed=embed)


@bot.tree.command(name="gamemanual", description="Get a link to the game manual")
async def game_manual(ctx: discord.Interaction):
    await ctx.response.defer()

    embed = discord.Embed(title="Game Manual", description="Here is the link to the game manual", color=0xf57f26)
    embed.add_field(name="Game Manual", value="[Game Manual](https://ftc-resources.firstinspires.org/file/ftc/game/manual)", inline=False)

    embed.set_footer(text=universal_footer)
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