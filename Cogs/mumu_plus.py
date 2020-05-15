import discord
import random
from discord.ext import commands
from discord.utils import get

Class MuMu_Support(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    
    @bot.event
    async def on_message(message):
        if message.author == client.user:
        return

        if message.content.startswith('$s'):
            # send a guess on how far away the shiny is. Playing around with random numbers
            # if it somehow guesses right people are going to freak out
            await message.channel.send('I predict a shiny in ' + str(random.randint(1, 10000)) + ' frames')

            return

        return
            
    
    
    
    def setup(bot):
        bot.add_cog(Pokemon(bot))
