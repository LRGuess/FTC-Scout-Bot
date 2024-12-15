import discord
import os
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv('URL')
universal_footer = os.getenv('UNI_FOOTER')

async def game_manual(ctx: discord.Interaction):
    await ctx.response.defer()

    embed = discord.Embed(title="Game Manual", description="Here is the link to the game manual", color=0xf57f26)
    embed.add_field(name="Game Manual", value="[Game Manual](https://ftc-resources.firstinspires.org/file/ftc/game/manual)", inline=False)

    embed.set_footer(text=universal_footer)
    await ctx.followup.send(embed=embed)