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
    # notify the log that it's ready
    print('We have logged in as {0.user}'.format(bot))



@bot.command()
@commands.check(is_dev_room)
async def woop(ctx):
    embed=discord.Embed(title="Woop Woop!", color=0xffc572)
    embed.set_image(url="https://img.pokemondb.net/artwork/wooper.jpg")
    await ctx.send(embed=embed)
    return

@bot.command(aliases = ["appeal", "appealing"])
@commands.check(is_dev_room)
async def peel(ctx):
    await ctx.send("https://www.youtube.com/watch?v=4yHijxLoAPA")
    return

@bot.command()
@commands.check(is_dev_room)
async def uncool(ctx):
    embed=discord.Embed(color=0xffc572)
    embed.set_image(url="https://cdn.discordapp.com/attachments/686356524385173553/707577611303256064/7lzcc2z1r2x41.png")
    await ctx.send(embed=embed)
    return

@bot.command()
@commands.check(is_dev_room)
async def tg(ctx):
    embed=discord.Embed(title="<:haunter:689169011866730720> Now calling TGAAM <:haunter:689169011866730720>", description="Please hold.", color=0xffc572)
    embed.add_field(name="...", value="...")
    embed.set_footer(text="Must be doing something `%important`")
    await ctx.send(embed=embed)
    return

@bot.command()
@commands.check(is_dev_room)
async def phan(ctx):
    embed=discord.Embed(description="it me", color=0xffc572)
    embed.set_thumbnail(url="https://i.imgur.com/yOS4rdj.png")
    await ctx.send(embed=embed)
    return

@bot.command()
@commands.check(is_dev_room)
async def turnip(ctx):
    embed=discord.Embed(description="https://discordapp.com/channels/681917060011655179/686356524385173553/709480670237294682", color=0xffc572)
    await ctx.send(embed=embed)
    return




# start the program
# I had to manually add the bot token to Heroku's config variables
bot.run(os.environ['TOKEN'])