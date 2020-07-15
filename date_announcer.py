import discord, os, random, asyncio, traceback, json
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
from discord.ext.commands import CheckFailure
from discord.ext.commands import MissingRequiredArgument
from datetime import datetime, timedelta

bot = commands.Bot(command_prefix='*')

calendar_update_send_time = '12:52'

async def timed_jobs():
    await bot.wait_until_ready()
    while not bot.is_closed():
        now = datetime.strftime(datetime.now(), '%H:%M') 

        # calendar events
        if now == calendar_update_send_time:
            guild = bot.get_guild(689079080892760125)
            channel = guild.get_channel(697060204571000903)

            send_date = datetime.strftime(datetime.now() + timedelta(days = 1), '%B-%d') 
            await post_events(channel, send_date)
            time = 90
        else:
            time = 30
        await asyncio.sleep(time)


@bot.command()
async def today(ctx):
    now = datetime.strftime(datetime.now(), '%B-%d') 
    await post_events(ctx.channel, now)
    return

@bot.command()
async def tomorrow(ctx):
    now = datetime.strftime(datetime.now() + timedelta(days = 1), '%B-%d') 
    await post_events(ctx.channel, now)
    return


@bot.command()
async def date(ctx, now):
    await post_events(ctx.channel, now)
    return

async def post_events(channel, now):
    with open('resources/ac_events.json') as f:
                data = json.load(f)

    date_details = data[now]
    embed=discord.Embed(title="Event plans for : " + now, description=date_details["event"], color=0xffc572)
    await channel.send(embed=embed)
    return



bot.loop.create_task(timed_jobs())
bot.run(os.environ['TOKEN'])