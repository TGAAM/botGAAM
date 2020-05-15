# import modules
# For hosting from Heroku/Github I had to include a Requirements.txt file with the following
'''
discord.py==1.3.3
psycopg2==2.8.5
'''

import discord
import os
import random
import asyncio
import traceback
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands import CheckFailure
from discord.ext.commands import MissingRequiredArgument

# dev roles
# prime, tinkerer
devRoles = [689120404664746018, 697890481568481311]

# dev channel whitelist
# bot-testing, bot-testing-2, bot-testing-3
whitelistChannelsDev = [697060204571000903, 698135978270916678, 698135987225886740]

# setup a discord client
bot = commands.Bot(command_prefix="!", case_insensitive=True, description="Coding testing Bot")


# don't work in DMs
@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None

async def is_dev_room(ctx):
    return (ctx.channel.id in whitelistChannelsDev)

async def is_dev(ctx):
    # look through the list of mod roles and check if the user has one
    for roleID in devRoles:
        role = ctx.guild.get_role(roleID)
        if (role in ctx.author.roles):
            # only need one match to be valid
            return True
    
    # nothing found so not a mod
    return False

# initial setup 
@bot.event
async def on_ready():
    cogs = ['cogs.mumu_plus']
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print("Problem with loading: " + str(cog))
            traceback.print_exc()

    # notify the log that it's ready
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
@commands.check(is_dev_room)
async def beep(ctx):
    await ctx.send("Boop!")
    return

@bot.command()
async def dynamax(ctx):
    await ctx.send("🙀 🙀 Are you really <:gmax_gengar:696490246057099304> Dynamaxing <:gmax_gengar:696490246057099304>?!?!?! 🤔 🤔 B-But have u checked the 📌 📌 pins?!!❗ I'm not 🙅 🙅‍♀️ allowing it!!! 🙏 🙏 Please, don't Dynamax ⛔ ⛔")
    return


# start the program
# I had to manually add the bot token to Heroku's config variables
bot.run(os.environ['TOKEN'])
