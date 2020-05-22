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



@bot.command(pass_context=True)
@commands.check(is_mod)
async def goodnight(ctx):
    for channelID in activeChannels:
        channel = ctx.guild.get_channel(channelID)
        role = ctx.guild.get_role(activeChannels[channelID])
        await channel.set_permissions(role, send_messages=True, read_messages=True)

    notifyRole = ctx.guild.get_role(689120404664746018)
    await ctx.send(notifyRole.mention + " Good night")

    return

@bot.command(pass_context=True)
@commands.check(is_mod)
async def goodmorning(ctx):
    for channelID in activeChannels:
        channel = ctx.guild.get_channel(channelID)
        role = ctx.guild.get_role(activeChannels[channelID])
        await channel.set_permissions(role, send_messages=True, read_messages=True)

    notifyRole = ctx.guild.get_role(689120404664746018)
    await ctx.send(notifyRole.mention + " Good morning")

    return




# start the program
# I had to manually add the bot token to Heroku's config variables
bot.run(os.environ['TOKEN'])