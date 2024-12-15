import discord

async def about(ctx: discord.Interaction):
    await ctx.response.defer()

    embed = discord.Embed(title="About", description="This bot is a Discord bot that uses the FTC Scout API to get information about teams and their statistics", color=0x00ff00)
    embed.add_field(name="Author", value="Liam Ramirez-Guess from 22212", inline=False)
    embed.add_field(name="Support Server", value="https://discord.gg/D4WUX7r3", inline=False)
    embed.add_field(name="FTC Scout", value="https://ftcscout.org", inline=False)
    embed.add_field(name="Version", value="1.0", inline=False)

    await ctx.followup.send(embed=embed)