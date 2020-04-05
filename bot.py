import discord



client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('%hi'):
        await message.channel.send('Hello!')

    if message.content.startswith('%test'):
        await message.channel.send(message.channel.name)

    if message.content.startswith('%giveaway') and message.channel.name == 'giveaway-announcements':
        await client.get_channel(694645573625708565).send('msg: ' + message.content)

client.run('Njk0NTU5OTk3Mjk1NzIyNjI3.XoNZgw.xQ1Gc25yMLpWOmCDGJdInhf4Zrg')
 
