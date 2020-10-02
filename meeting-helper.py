import discord
import re

import requests
import json

from discord.ext import commands
from discord.ext.commands import CommandNotFound

from prioritylevels import Priorities

bot = commands.Bot(command_prefix='!')
priorities = json.loads('{"message": "No answer from GitLab"}')

mp_topics = []
pa_token = ""
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {   0.user}'.format(client))

@bot.command()
async def commands(ctx):
    message = ">>> You can add topics to the agenda with the command: **!addtopic** <topic-text> \n"\
        "You can see the current topics of the agenda with: **!showagenda** \n"\
        "You can clear the agenda with: **!clearagenda** \n"\
        "You can delete topics from the agenda with: **!deletetopic** (you will be prompted after sending this command) \n"\
        "You can see the full agenda (gitlab boards aswell) with: **!topic** \n"
    await ctx.send(message)

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def addtopic(ctx, *, arg):
    response = arg
    mp_topics.append(response.capitalize())
    await ctx.send('You have added a new topic: {}'.format(response))

@bot.command()
async def showagenda(ctx):
    response = "__**Meeting points**__ \n"
    index = 1
    for topic in mp_topics:
        response = response + "> #{}: {} \n".format(index, topic)
        index += 1
    await ctx.send(response)

@bot.command()
async def clearagenda(ctx):
    mp_topics.clear()
    await ctx.send('Topics cleared!')

@bot.command()
async def deletetopic(ctx):
    response = "**Please specify which topic you want to remove from the list! (1, 2, 3...)**\n"
    index = 1
    if not len(mp_topics):
        return
    
    else:
        for topic in mp_topics:
            response = response + "> #{}: {} \n".format(index, topic)
            index += 1
        await ctx.send(response)
    msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    try:
        msg = int(msg.content)
    except ValueError:
        await ctx.send('Input is not a number!')
    else:
        if msg >= 0 and msg < len(mp_topics):
            del mp_topics[msg-1]
            await ctx.send('Topic #{} successfully deleted!'.format(msg))
        else:
            await ctx.send('Index is out of bounds!')

@bot.command()
async def topic(ctx):
    global pa_token
    if not pa_token:
        await ctx.send("Set the personal access token first with **!config** <token>")
        return
    else:
        priorities = Priorities(pa_token)
    try:
        if priorities.response['message']:
            await ctx.send("Error! Set new personal acces token with **!config** <token>")
    except:
        None
    priorities.get_topics()
    hpresponse = priorities.high_prio_message
    lpresponse = priorities.low_prio_message
    await showagenda(ctx = ctx)
    await ctx.send(hpresponse)
    await ctx.send(lpresponse)

@bot.command()
async def config(ctx, arg):
    global pa_token
    pa_token = arg
    await ctx.send("Token set!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Command not recognized. Use **!commands** for available commands.")

#Change to your bot's token
bot.run('TOKEN')
