import discord
import random
from discord.ext import commands
from discord.utils import get

class MuMu_plus (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith('$s'):
            # send a guess on how far away the shiny is. Playing around with random numbers
            # if it somehow guesses right people are going to freak out
            #await message.channel.send('I predict a shiny in ' + str(random.randint(1, 10000)) + ' frames')
            await message.channel.send("Remember that the best seeds are reserved for the best hosts, those of Team Teal <:wigglyteal:720089522766872606>")

            return

        return
            
    
    
def setup(bot):
    bot.add_cog(MuMu_plus(bot))
