import discord
import os
import random
import psycopg2


DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
client = discord.Client()
cursor = conn.cursor()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    #setup the table if it's not already
    sqlTable = "create table if not exists users(user_id bigint, hi_count int);"
    cursor.execute(sqlTable)
    conn.commit()
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('%beep'):
        await message.channel.send('Boop!')
        
    if message.content.startswith('$s'):
        await message.channel.send('I predict a shiny in ' + str(random.randint(1, 10000)) + ' frames')

    if (message.channel == client.get_channel(696864617653076078)):
        if message.content.startswith('%g start'):
            await message.channel.send('Creating giveaway')

    if (message.content.startswith('$hi')):
        hiCount = 1 + int(cursor.execute("select hi_count from users where user_id = " + str(message.author.id)) or 0)
        if (hiCount == 1):
            cursor.execute("insert into users(user_id, hi_count) values ("+str(message.author.id)+", 1)")
            conn.commit()

        await message.channel.send("You've said hi to MuMu " + str(hiCount) + " times since I started counting" )

        cursor.execute('update users set hi_count = ' + str(hiCount) + "where user_id = " + str(message.author.id))
        conn.commit()

'''
    if message.content.startswith('%hi'):
        await message.channel.send('Hello!')
    if message.content.startswith('%test'):
        await message.channel.send(message.channel.name)
    if message.content.startswith('%giveaway') and message.channel.name == 'giveaway-announcements':
        await client.get_channel(694645573625708565).send('msg: ' + message.content)
'''


client.run(os.environ['TOKEN'])
