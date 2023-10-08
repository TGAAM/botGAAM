# import modules
# For hosting from Heroku/Github I had to include a Requirements.txt file with the following
'''
discord.py==1.3.3
psycopg2==2.8.5
'''

from operator import truediv
import discord
import os
import random
import asyncio
import traceback
import emoji

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
# bot-testing, bot-testing-2, bot-testing-3, robots
whitelistChannelsDev = [697060204571000903, 698135978270916678, 698135987225886740, 778751730233770015]

# active channels dict
# super-mumu-world: legends, mumu-bros: minions
activeChannels = {689084632150573118:712967008743850084, 689079607093493780:689533761767079993}


# setup a discord client
varIntents = discord.Intents.default()
varIntents.message_content = True
varIntents.reactions = True
varIntents.members = True
bot = commands.Bot(command_prefix="!", case_insensitive=True, description="Coding testing Bot", intents = varIntents)


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


@bot.listen()
async def on_message(message):
        if message.author == bot.user:
            return

        # condensed logging
        # mumu-log, mumu-trade
        logChannels = [689976669930651725, 690534943138512896]

        if (message.channel.id in logChannels):
            copyTexts = ["is now trading", "Found Trading Partner", "Unexpected behavior", "Resetting bot position"]

            for text in copyTexts:
                if text in message.content:
                    # mumu-condensed-log
                    outputChannel = message.guild.get_channel(714810032142811207) 
                    await outputChannel.send(message.content)
                    return
        return

@bot.command(pass_context=True)
@commands.check(is_mod)
async def goodnight(ctx):
    for channelID in activeChannels:
        channel = ctx.guild.get_channel(channelID)
        role = ctx.guild.get_role(activeChannels[channelID])
        await channel.set_permissions(role, send_messages=False, read_messages = True)

    notifyRole = ctx.guild.get_role(689120404664746018)
    await ctx.send(notifyRole.mention + " Good night")

    return

@bot.command(pass_context=True)
@commands.check(is_mod)
async def goodmorning(ctx):
    for channelID in activeChannels:
        channel = ctx.guild.get_channel(channelID)
        role = ctx.guild.get_role(activeChannels[channelID])
        await channel.set_permissions(role, send_messages=True, read_messages = True)

    notifyRole = ctx.guild.get_role(689120404664746018)
    await ctx.send(notifyRole.mention + " Good morning")

    return

@bot.command()
@commands.check(is_dev_room)
async def beep(ctx):
    await ctx.send("Boop!")
    return

@bot.command()
@commands.check(is_dev_room)
async def ping(ctx):
    await ctx.send("Pong!")
    return

@bot.command()
async def dynamax(ctx):
    await ctx.send("🙀 🙀 Are you really <:gmax_gengar:696490246057099304> Dynamaxing <:gmax_gengar:696490246057099304>?!?!?! 🤔 🤔 B-But have u checked the 📌 📌 pins?!!❗ I'm not 🙅 🙅‍♀️ allowing it!!! 🙏 🙏 Please, don't Dynamax ⛔ ⛔")
    return

@bot.event
async def on_raw_reaction_add(reaction):
    if str(reaction.emoji) == "<:wigglygreen:810539771759689778>":
        msgGuild = bot.get_guild(reaction.guild_id)
        msgChannel = msgGuild.get_channel(reaction.channel_id)
        oldMsg = await msgChannel.fetch_message(reaction.message_id) 
        newMsg = oldMsg.content

        newMsg = emoji.demojize(newMsg,delimiters=("",""))

        newMsg = newMsg.replace('black_large_square', '<:typeDark:811060133643288636>')
        newMsg = newMsg.replace('green_square', '<:typeBug:811060133235916802>')
        newMsg = newMsg.replace('yellow_square', '<:typeElectric:811060168292040764>')

        await oldMsg.channel.send(newMsg)
    return

# error handling
@bot.event
async def on_command_error(ctx, error):
    # ignore errors that are invalid commands or calls from failed checks for now
    if isinstance(error, CommandNotFound):
        return
    elif isinstance(error, CheckFailure):
        return
    elif isinstance(error, MissingRequiredArgument):
        await ctx.send("You need to include more details for this command")
        return

    raise error

# start the program
# I had to manually add the bot token to Heroku's config variables
bot.run(os.environ['TOKEN'])
