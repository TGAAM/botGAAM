import discord
import os
import random
import psycopg2


DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
client = discord.Client()

@client.event
async def on_ready():
    #setup the table if it's not already
    cursor = conn.cursor()

    # uncomment to reset the table on next/each load
    #cursor.execute("drop table users")
    #conn.commit()
    
    sqlTable = "create table if not exists users(user_id bigint not null, hi_count int, check_count int, primary key(user_id));"
    cursor.execute(sqlTable)
    conn.commit()

    print('We have logged in as {0.user}'.format(client))
    

@client.event
async def on_message(message):
    cursor = conn.cursor()

    if message.author == client.user:
        return
    if message.content.startswith('%beep'):
        await message.channel.send('Boop!')
        
    if message.content.startswith('$s'):
        cursor.execute("select count(*) from users where user_id = " + str(message.author.id))
        userExists = cursor.fetchone()[0]

        if (userExists == 0):
            cursor.execute("insert into users(user_id, check_count) values ("+str(message.author.id)+", 1)")
            conn.commit()
        else:
            cursor.execute("select check_count from users where user_id = " + str(message.author.id))
            checkCount = 1 + cursor.fetchone()[0]
            cursor.execute("update users set check_count = " + str(checkCount) + "where user_id = " + str(message.author.id))
            conn.commit()

        await message.channel.send('I predict a shiny in ' + str(random.randint(1, 10000)) + ' frames')


    if (message.content.startswith('$hi')):
        cursor.execute("select count(*) from users where user_id = " + str(message.author.id))
        userExists = cursor.fetchone()[0]

        if (userExists == 0):
            cursor.execute("insert into users(user_id, hi_count) values ("+str(message.author.id)+", 1)")
            conn.commit()
        else:
            cursor.execute("select hi_count from users where user_id = " + str(message.author.id))
            hiCount = 1 + cursor.fetchone()[0]
            cursor.execute("update users set hi_count = " + str(hiCount) + "where user_id = " + str(message.author.id))
            conn.commit()


    if (message.content.startswith('$dynamax')):
            await message.channel.send("🙀 🙀 Are you really <:gmax_gengar:696490246057099304> Dynamaxing <:gmax_gengar:696490246057099304>?!?!?! 🤔 🤔 B-But have u checked the 📌 📌 pins?!!❗ I'm not 🙅 🙅‍♀️ allowing it!!! 🙏 🙏 Please, don't Dynamax ⛔ ⛔")


    if (message.content.startswith('%fetch')):
        msgResults = ''

        inputStr = message.content.split(' ')

        if (len(inputStr) > 2):
            await message.channel.send('Too many input parameters')
            return

        cursor.execute("select count(*) from users where user_id = " + inputStr[1])
        userExists = cursor.fetchone()[0]
        

        if (userExists == 0):
            msgResults = 'User not found'
        else:
            cursor.execute("select * from users where user_id = " + inputStr[1])
            msgResults = str(cursor.fetchone())

        await message.channel.send(msgResults)





'''
    if message.content.startswith('%hi'):
        await message.channel.send('Hello!')
    if message.content.startswith('%test'):
        await message.channel.send(message.channel.name)
    if message.content.startswith('%giveaway') and message.channel.name == 'giveaway-announcements':
        await client.get_channel(694645573625708565).send('msg: ' + message.content)
'''


client.run(os.environ['TOKEN'])
