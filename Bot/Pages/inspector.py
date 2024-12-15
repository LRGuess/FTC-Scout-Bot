import discord
from discord.ui import View

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