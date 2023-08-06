import discord
import json
from student import Student
from discord.ext import commands


with open('./config.json', 'r') as cfg:
    data = json.load(cfg)
    token = data["token"]

print(token)
CHANNEL_ID = '1079912337571598438'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
users = {}
s = None


@bot.event
async def on_ready():
    print("Bot is now running")


@bot.command()
async def ping(ctx):
    await ctx.send('pong!')


@bot.command(help="creates a new student, must give it a uni")
async def createuser(ctx):
    username = str(ctx.author)
    uni = ctx.message.content.split(' ')[1]
    print(uni)
    print(username)
    s = Student(username, uni)
    users[username] = s
    print(s)
    print(users)
    await ctx.send('created!')


@bot.command()
async def addclass(ctx):
    username = str(ctx.author)
    users[username].add_class(ctx.message.content.split(' ')[1])
    print(users[username])

    await ctx.send('Added class!')


@bot.command()
async def addprof(ctx):
    await ctx.send('Added prof!')


# @bot.command()
# async def getusernames(ctx):
#     await ctx.send(df['username'])

# @bot.command()
# async def getclasses(ctx):
#     await ctx.send(df['class_name'][0])

# @bot.command()
# async def getunis(ctx):
#     await ctx.send(df['uni'])

bot.run(token)
