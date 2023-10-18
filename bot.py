# bot.py
import os
import discord
from dotenv import load_dotenv
import random
from discord.ext import commands
import subprocess
import requests
import json
import openai

# Set your OpenAI API key
openai.api_key = ""



load_dotenv('./.env')
# TOKEN = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv('DISCORD_GUILD')
# print(TOKEN, GUILD)
TOKEN = ''
GUILD = "scooter really wanted to join"
intents = discord.Intents.all()
# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name + '#' + member.discriminator for member in guild.members])
    print(f'Guild Members:\n - {members}')
    print("\nBot Ready!")


# @bot.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )


@bot.command(name = "darkhumor", help = "!darkhumor Responds with dark jokes",)
async def yo_insult(ctx):
    response = random.choice(open("darkhumor.txt","r").read().split("\n\n"))
    await ctx.send(response)


@bot.command(name = "yomamma", help = "!yomamma Responds with Yo Momma jokes specifically")
async def yo_insult(ctx):
    response = random.choice(open("yomamma.txt","r").readlines())
    await ctx.send(response)

@bot.command(name = "dmdarren", help = "!dmdarren DM's saucyeti")
async def dm_darren(ctx):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    darren = discord.utils.find(lambda g: g.name == "lindarren" and g.discriminator == "0", guild.members)
    await ctx.send("Message Sent!")
    await darren.create_dm()
    await darren.dm_channel.send('HUGE PP INCOMING\n8==========================================D')

@bot.command(name = "dm", help = "!dm <Username> DM's given user (ONLY NAME) given message")
async def dm(ctx,user):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    user = discord.utils.find(lambda g: g.name == user, guild.members)
    message = ctx.message.content[ctx.message.content.index(user.name) + len(user.name):]
    try:
        await user.create_dm()
        await user.dm_channel.send(message)
        await ctx.send("Message Sent!")
    except:
        await ctx.send("Error")


@bot.command(name = "dm_tag", help = "!dm_tag <User#1234> DM's given user with tag (User#1234) given message")
async def dm(ctx,user):
    guild = discord.utils.get(bot.guilds, name=GUILD)
    user = discord.utils.find(lambda g: g.name == user[:user.index('#')] and g.discriminator == user[user.index('#')+1:], guild.members)
    message = ctx.message.content[ctx.message.content.index(user.name + "#" + user.discriminator) + len(user.name + "#" + user.discriminator):]
    await ctx.send("Message Sent!")
    await user.create_dm()
    await user.dm_channel.send(message)

@bot.command(name = "pp", help = "!pp <length> Responds with pp of given length")
async def pp(ctx,length:int):
    await ctx.send("8" + "".join(["="] * min(length,1998)) + "D")

@bot.command(name="gpt", help="!gpt <prompt> Responds with gpt3.5 response")
async def gpt2(ctx):
    # Make the API call
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            # {"role": "system", "content": "You are a"},
            {"role": "user", "content": ctx.message.content[ctx.message.content.index("!gpt") + len("!gpt"):]}
        ]
    )
    result = response['choices'][0]['message']['content']
    # Print 2000 characters of response at a time
    for i in range(0, len(result), 2000):
        await ctx.reply(result[i:i+2000])
    # await ctx.reply(response['choices'][0]['message']['content'])

@bot.command(name="gpt2", help="!gpt2 <prompt> Responds with uncensored ai response")
async def gpt2(ctx):
    url = "http://localhost:8080/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "luna-ai-llama2",
        "messages": [{"role": "user", "content": ctx.message.content[ctx.message.content.index("!gpt2") + len("!gpt2"):]}],
        "temperature": 0.9
    }

    response = requests.post(url, headers=headers, json=data)
    await ctx.reply(json.loads(response.text)['choices'][0]['message']['content'])

special_chars = ['\'', '`', '_', '~', '|', '']
def get_fun_fact():
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
    response = requests.get(url)
    data = response.json()
    return "```" + data['text'] + "```"

@bot.command(name="fun", help="!fun Responds with a random fun fact")
async def fun(ctx):
    await ctx.reply(get_fun_fact())


@bot.event
async def on_message(message):
    if type(message.channel) == discord.channel.TextChannel and message.channel.name == 'bot-test':
        # if message.author.name in ['tanayp', 'nprdeep', 'aeroani', 'chinmayraghvendran']:
        #     await message.reply('monkey')
        # elif message.author.name in ['lindarren', '1glub', 'k_wu', 'jaydenclim', 'scooter1946', 'hafnium780', 'boeingiscool']:
        #     await message.reply('dog eater')
        await bot.process_commands(message)

# subprocess.run(['./LocalAI/local-ai', '--models-path', './LocalAI/models/', '--debug'])
bot.run(TOKEN)

