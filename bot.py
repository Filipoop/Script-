import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

class SplitStealView(View):
    def __init__(self, user1: discord.User, user2: discord.User, for_what: str):
        super().__init__(timeout=60)
        self.user1 = user1
        self.user2 = user2
        self.for_what = for_what
        self.user1_choice = None
        self.user2_choice = None

        @discord.ui.button(label='Split', style=discord.ButtonStyle.green)
        async def split_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user == self.user1:
                self.user1_choice = 'split'
                elif interaction.user == self.user2:
                    self.user2_choice = 'split'
                    await interaction.response.send_message('You chose to split!', ephemeral=True)
                    await self.check_choices(interaction)

                    @discord.ui.button(label='Steal', style=discord.ButtonStyle.red)
                    async def steal_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                        if interaction.user == self.user1:
                            self.user1_choice = 'steal'
                            elif interaction.user == self.user2:
                                self.user2_choice = 'steal'
                                await interaction.response.send_message('You chose to steal!', ephemeral=True)
                                await self.check_choices(interaction)

                                async def check_choices(self, interaction: discord.Interaction):
                                    if self.user1_choice and self.user2_choice:
                                        if self.user1_choice == 'split' and self.user2_choice == 'split':
                                            await interaction.channel.send(f'{self.for_what} has been split!')
                                            elif self.user1_choice == 'steal' and self.user2_choice == 'split':
                                                await interaction.channel.send(f'{self.user1.mention} stole {self.for_what} from {self.user2.mention}!')
                                                elif self.user1_choice == 'split' and self.user2_choice == 'steal':
                                                    await interaction.channel.send(f'{self.user2.mention} stole {self.for_what} from {self.user1.mention}!')
                                                    else:
                                                        await interaction.channel.send(f'{self.user1.mention} and {self.user2.mention} both stole! They both win nothing!')
                                                        self.stop()

                                                        @bot.event
                                                        async def on_ready():
                                                            print(f'Logged in as {bot.user}')

                                                            @bot.tree.command(name='splitsteal', description='Split or steal from another user')
                                                            async def splitsteal(interaction: discord.Interaction, user1: discord.User, user2: discord.User, for_what: str):
                                                                view = SplitStealView(user1, user2, for_what)
                                                                await user1.send(f'You have been challenged to split or steal {for_what} from {user2.mention}!', view=view)
                                                                await user2.send(f'You have been challenged to split or steal {for_what} from {user1.mention}!', view=view)
                                                                await interaction.response.send_message('The challenge has been sent to both users!', ephemeral=True)

                                                                bot.run('YOUR_BOT_TOKEN')
