# bot.py
import os
import discord
from dotenv import load_dotenv
import random
from discord.ext import commands




load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.all()
#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)


# @client.event
# async def on_ready():
#     guild = discord.utils.get(client.guilds, name=GUILD)
#     print(
#         f'{client.user} is connected to the following guild:\n'
#         f'{guild.name}(id: {guild.id})'
#     )
#     members = '\n - '.join([member.name for member in guild.members])
#     print(f'Guild Members:\n - {members}')


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name + '#' + member.discriminator for member in guild.members])
    print(f'Guild Members:\n - {members}')


# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@bot.command(name = "yo_insult!", help = "Responds with Yo __ jokes")
async def yo_insult(ctx):
    response = random.choice(open("insults.txt","r").readlines())
    await ctx.send(response)

@bot.command(name = "dmdarren!", help = "DM's saucyeti")
async def dm_darren(ctx):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    darren = discord.utils.find(lambda g: g.name == "saucyeti" and g.discriminator == "7095", guild.members)
    await ctx.send("Message Sent!")
    await darren.create_dm()
    await darren.dm_channel.send('HUGE PP INCOMING\n8==========================================D')

@bot.command(name = "dm!", help = "DM's given user (ONLY NAME) given message")
async def dm(ctx,user):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    user = discord.utils.find(lambda g: g.name == user, guild.members)
    message = ctx.message.content[ctx.message.content.index(user.name) + len(user.name):]
    await ctx.send("Message Sent!")
    await user.create_dm()
    await user.dm_channel.send(message)

@bot.command(name = "dm_tag!", help = "DM's given user with tag (User#1234) given message")
async def dm(ctx,user):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    user = discord.utils.find(lambda g: g.name == user[:user.index('#')] and g.discriminator == user[user.index('#')+1:], guild.members)
    message = ctx.message.content[ctx.message.content.index(user.name + "#" + user.discriminator) + len(user.name + "#" + user.discriminator):]
    await ctx.send("Message Sent!")
    await user.create_dm()
    await user.dm_channel.send(message)

#client.run(TOKEN)
bot.run(TOKEN)