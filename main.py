from replit import db
import os
os.system("pip install py-cord==2.0.0b1")
import discord
from discord.ext import commands
from keep_alive import keep_alive
keep_alive()
import random
import asyncio
import time, datetime, requests
client = commands.Bot(command_prefix=';', intents = discord.Intents.all())
client.remove_command('help')

@client.event
async def on_ready():
    print(f"Bot's ping: {round(client.latency * 1000)}ms")
    print("Client ID: 1046470991745921185")
    print("Developed by: maxwalks#3479")
    print('Bot is ready.')

async def bot_activity():
  await client.wait_until_ready()
  while True:
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))
    await asyncio.sleep(10)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Dabloons"))
    await asyncio.sleep(10)

@client.slash_command(description="Help Command.")
async def help(ctx):
    icon = str(ctx.guild.icon.url)
    name = str(ctx.guild.name)
    embed = discord.Embed(
        title = name + ' Help Center',
        description = 'Displays all the commands.',
        color = discord.Color.dark_grey()
    )
    embed.set_footer(text=f'Requested By {ctx.author}')
    embed.set_thumbnail(url=icon)
    embed.add_field(name='/server', value='`Displays server info.`', inline=True)
    embed.add_field(name='/info', value='`Displays bot info.`', inline=True)
    embed.add_field(name='/givebrain <user>', value='`Gives somoene a free brain.`', inline=False)
    embed.add_field(name='/ping', value='`Displays bot ping`', inline=True)
    embed.add_field(name='/userinfo <user>', value="`Displays the user's info.`", inline=True)
    embed.add_field(name="/meme", value="`Displays a meme from Reddit.`")
    await ctx.respond(embed=embed)

@client.slash_command(description="Normal slash command for test.")
async def hello(ctx):
    await ctx.respond(f"Hello {ctx.author.name}!")

@client.slash_command(description="Setup your Dabloons bank.")
async def dabloons(ctx):
    await ctx.respond("Creating your bank..")
    db[f"{ctx.author.name}"] = "0"
    await asyncio.sleep(2)
    await ctx.send(f"Succesfully created a bank for {ctx.author.name}")

@client.slash_command(description="Add Dabloons to your bank.")
async def add(ctx, amount):
    await ctx.respond("Adding Dabloons..")
    value = db[f"{ctx.author.name}"]
    db[f"{ctx.author.name}"] = value + amount
    await asyncio.sleep(2)
    await ctx.send(f"I have added {amount} Dabloons to your account.")

@client.slash_command(description="Resets all your dabloons.")
async def reset(ctx):
    await ctx.respond("Resetting Dabloons..")
    db[f"{ctx.author.name}"] = "0"
    await ctx.send("Your Dabloons are now reset.")

@client.slash_command(description="Displays your amount of Dabloons.")
async def bank(ctx):
    await ctx.respond("Retrieving Dabloons..")
    value = db[f"{ctx.author.name}"]
    await asyncio.sleep(2)
    await ctx.send(f"You have {value} Dabloons.")

@client.slash_command(description="Removes Dabloons from bank")
async def remove(ctx, amount):
    await ctx.respond("Removing Dabloons..")
    value = db[f"{ctx.author.name}"]
    db[f"{ctx.author.name}"] = value - amount
    await asyncio.sleep(2)
    await ctx.send(f"I have removed {amount} Dabloons from your bank.")
  
@client.slash_command(description="Returns the bot's ping")
async def ping(ctx):
  before = time.monotonic()
  await ctx.respond("Fetching Ping..", delete_after=0)
  ping = (time.monotonic() - before) * 1000
  em = discord.Embed(title="PONG!🏓", description=f"My Ping is `{int(ping)} ms`")
  em.set_author(name=ctx.author)
  em.timestamp = datetime.datetime.utcnow()
  await ctx.respond(embed=em)

@client.slash_command(description="Returns random memes from reddit.")
async def meme(ctx):
  res = requests.get("https://meme-api.herokuapp.com/gimme/memes").json() # Getting Requests
  meme_title = res['title']
  meme_link = res['postLink']
  meme_img = res['url']
  meme_author = res['author']
  meme_likes = res['ups']
  # Creating Embed
  x = discord.Embed(title=f"{meme_title}", url=f"{meme_link}")
  x.set_image(url=meme_img)
  x.set_footer(text=f"Redditor: {meme_author} • 👍 {meme_likes} | Requested By {ctx.author}")
  x.set_author(name=meme_author, url=f"https://www.reddit.com/user/{meme_author}", icon_url='https://media.discordapp.net/attachments/880439870374436864/882131944391999488/Reddit.png?width=417&height=417')
  await ctx.respond(embed=x)

@client.slash_command(description="Gives somoene a free brain.")
async def givebrain(ctx, member : discord.Member):
    await ctx.respond(f'{member.mention}, you have been given a free brain by {ctx.author.mention} :brain:')

@client.slash_command(description="Displays the user's info.")
async def userinfo(ctx, user: discord.Member):
    await ctx.respond("The users name is: `{}`".format(user.name))
    await ctx.send("The users ID is: `{}`".format(user.id))
    await ctx.send("The users highest role is: `{}`".format(user.top_role))
    await ctx.send("The user joined at: `{}`".format(user.joined_at))
    await ctx.send("The user's account creation date is: `{}`".format(user.created_at))

@client.slash_command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx):
    message = await ctx.respond('Giveaway')
    await ctx.message.add_reaction(thumb_up)
    message = message.id
    users = [user async for user in reaction.users()]
    winner = random.choice(users)
    await ctx.respond(f'{winner} has won the raffle.')


BOT_TOKEN = os.environ['BOT_TOKEN']
client.loop.create_task(bot_activity())
client.run(BOT_TOKEN)