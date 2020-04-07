# import modules
#For hosting from Heroku/Github I had to include a Requirements.txt file with the following
'''
discord.py==1.3.3
psycopg2==2.8.5
'''

import discord
import os
import random
import psycopg2

# the default database URL is automatically created when you get Postgres
DATABASE_URL = os.environ['DATABASE_URL']

# create a connection to the database and setup a discord client
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
client = discord.Client()

# initial setup 
@client.event
async def on_ready():
    #setup the table if it's not already
    
    # create a cursor to execute SQL commands
    cursor = conn.cursor()

    # uncomment to reset the table on next/each load
    #cursor.execute("drop table users")
    #conn.commit()
    
    # make a table Users(user_id, hi_count, check_count)
    # user_id requires a value and must be unique in the table
    # hi_count and check_count default to 0 if no value is set for them (otherwise they would have a null value)
    sqlTable = "create table if not exists users(user_id bigint not null, hi_count int default 0, check_count int default 0, primary key(user_id));"
    cursor.execute(sqlTable)

    # make sure to commit after writing any data like create/insert/update
    conn.commit()

    # notify the log that it's ready
    print('We have logged in as {0.user}'.format(client))
    

# message posted
@client.event
async def on_message(message):
    # create a cursor to execute SQL commands
    # I think we want to make it in here so each event gets its own
    # I'm not very familiar with asynchronous stuff so that could be wrong
    cursor = conn.cursor()

    # don't respond to itself
    if message.author == client.user:
        return

    # simple answer/reply command
    if message.content.startswith('%beep'):
        await message.channel.send('Boop!')


    # testing including emojis
    # $ command playing off the April Fool's joke in PMR    
    if (message.content.startswith('$dynamax')):
            await message.channel.send("🙀 🙀 Are you really <:gmax_gengar:696490246057099304> Dynamaxing <:gmax_gengar:696490246057099304>?!?!?! 🤔 🤔 B-But have u checked the 📌 📌 pins?!!❗ I'm not 🙅 🙅‍♀️ allowing it!!! 🙏 🙏 Please, don't Dynamax ⛔ ⛔")


    # watch for someone to request a seed check
    if message.content.startswith('$s'):
        # check if the user is already in the table
        cursor.execute("select count(*) from users where user_id = " + str(message.author.id))

        # fetch returns a tuple/list, you need to grab the element even if it's the only one
        userExists = cursor.fetchone()[0]

        if (userExists == 0):
            # if they don't exist add them to the table
            # hi_count isn't set here so it will default to 0
            cursor.execute("insert into users(user_id, check_count) values ("+str(message.author.id)+", 1)")

            # remember to commit
            conn.commit()
        else:
            # the user does exist in the table

            # get the check_count
            cursor.execute("select check_count from users where user_id = " + str(message.author.id))

            
            # we're querying on a unique value (user_id) so only one row will be returned
            # if you want to run a query that could include multiple results you can use .fetchall() and loop through the results
            checkCount = 1 + cursor.fetchone()[0]

            # update the table with the incremented count
            cursor.execute("update users set check_count = " + str(checkCount) + "where user_id = " + str(message.author.id))
            conn.commit()

        # send a guess on how far away the shiny is. Playing around with random numbers
        # if it somehow guesses right people are going to freak out
        await message.channel.send('I predict a shiny in ' + str(random.randint(1, 10000)) + ' frames')


    # functionally the same as the seed check counter
    # find the user, create a record if one doesn't exist
    # update the total
    # no need to actually write to the chat if you just want to track stuff
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


    # retrieve stored data 
    if (message.content.startswith('%fetch')):
        # I know this is Python but I still like initializing variables if I'm not immediately using them
        msgResults = ''

        # split the input into parameters on spaces
        # you could use other delimiters like | (pipe) or a more complex split depending on what you need
        inputStr = message.content.split(' ')

        # error message example
        # check if the input is too long
        if (len(inputStr) > 2):
            await message.channel.send('Too many input parameters')
            return

        # check if the user is in the table
        cursor.execute("select count(*) from users where user_id = " + inputStr[1])
        userExists = cursor.fetchone()[0]

        if (userExists == 0):
            # no records in the table means they haven't done a seed check or $hi since the last table wipe
            msgResults = 'User not found'
        else:
            # select * returns all the values for the row
            cursor.execute("select * from users where user_id = " + inputStr[1])

            # str() to format the result. May not be neccessary in Python
            # for a real project you would want to format it nicer by mixing regular text in with the results
            msgResults = str(cursor.fetchone())

        # post the results
        await message.channel.send(msgResults)





'''
    if message.content.startswith('%hi'):
        await message.channel.send('Hello!')
    if message.content.startswith('%test'):
        await message.channel.send(message.channel.name)
    if message.content.startswith('%giveaway') and message.channel.name == 'giveaway-announcements':
        await client.get_channel(694645573625708565).send('msg: ' + message.content)
'''

# start the program
# I had to manually add the bot token to Heroku's config variables
client.run(os.environ['TOKEN'])
