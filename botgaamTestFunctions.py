import discord
import os
import random
import asyncio
import traceback
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands import CheckFailure
from discord.ext.commands import MissingRequiredArgument

# mod roles
# prime
modRoles = [689120404664746018]

# dev roles
# prime, tinkerer
devRoles = [689120404664746018, 697890481568481311]

# dev channel whitelist
# bot-testing, bot-testing-2, bot-testing-3
whitelistChannelsDev = [697060204571000903, 698135978270916678, 698135987225886740]

# active channels dict
# super-mumu-world: legends, mumu-bros: minions
activeChannels = {689084632150573118:712967008743850084}


# setup a discord client
bot = commands.Bot(command_prefix="*", case_insensitive=True, description="Coding testing Bot")



# don't work in DMs
@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None

async def is_dev_room(ctx):
    return (ctx.channel.id in whitelistChannelsDev)

async def is_mod(ctx):
    # look through the list of mod roles and check if the user has one
    for roleID in modRoles:
        role = ctx.guild.get_role(roleID)
        if (role in ctx.author.roles):
            # only need one match to be valid
            return True
    
    # nothing found so not a mod
    return False

async def is_dev(ctx):
    # look through the list of mod roles and check if the user has one
    for roleID in devRoles:
        role = ctx.guild.get_role(roleID)
        if (role in ctx.author.roles):
            # only need one match to be valid
            return True
    
    # nothing found so not a dev
    return False

# initial setup 
@bot.event
async def on_ready():
    # notify the log that it's ready
    print('We have logged in as {0.user}'.format(bot))



@bot.listen()
async def on_message(message):
        if message.author == bot.user:
            return

        # condensed logging
        # bot-testing1, bot-testing3
        logChannels = [697060204571000903, 698135987225886740]

        if (message.channel.id in logChannels):
            copyTexts = ["is now trading", "Found Trading Partner", "Unexpected behavior", "Resetting bot position"]

            for text in copyTexts:
                if text in message.content:
                    # bot-testing2
                    outputChannel = message.guild.get_channel(698135978270916678) 
                    await outputChannel.send(message.content)
                    return


        return




# start the program
# I had to manually add the bot token to Heroku's config variables
bot.run(os.environ['TOKEN'])