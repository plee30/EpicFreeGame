import discord
import os
import sqlite3
import free
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
TOKEN = os.environ.get("DISCORD_TOKEN")

# intents = discord.Intents.default()
# intents.message_content = True

scheduler = AsyncIOScheduler()
scheduler.start()

conn = sqlite3.connect('channel_ids.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS channels(
            channel_id INTEGER UNIQUE)""")
c.execute("""CREATE TABLE IF NOT EXISTS games(
            game_name TEXT UNIQUE)""")

bot = discord.Bot()

# On Ready check
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await check_schedule()

# Wrapper for admin/owner check
def is_admin_or_owner():
    async def admin_or_owner_check(ctx):
        return ctx.author.guild_permissions.administrator or await bot.is_owner(ctx.author)
    return commands.check(admin_or_owner_check)
        
# Function to check the current Epic Games promotions and schedule jobs & post current promotions.
async def check_schedule():
    promos = free.get_promos()
    cur = promos.get("current")
    fut = promos.get("future")
    if cur:
        # Function to send message in appropriate channel with cur information.
        await freegames_auto(cur)
    if fut:
        # Function to schedule a check on the date and time of the next promotion
        await add_future_task(fut[0])
    else:
        # If no future promo, schedule to check a week later
        await add_future_task(free.no_promo())

# Function to add a future task
async def add_future_task(future_promo_datetime):
    scheduler.add_job(check_schedule, 'date', run_date=future_promo_datetime)

# Function to post current free promotion
async def freegames_auto(cur):
    # Checks table if this game has been sent
    c.execute("SELECT game_name FROM games")
    result = c.fetchall()
    games_in_table = [row[0] for row in result]
    if cur[2] not in games_in_table:
        embed = discord.Embed(
            title = "Free Game",
            description = cur[0],
            color = discord.Color.green()
        )
        c.execute("SELECT channel_id FROM channels")
        channel_list = c.fetchall()
        embed.set_image(url=cur[1])
        for each in channel_list:
            each = int(str(each)[1:-2])
            channel = bot.get_channel(each)
            await channel.send(embed=embed)
        c.execute(
            "INSERT OR IGNORE INTO games (game_name) VALUES (?)", (cur[2],)
        )
        conn.commit()
        

# Define a command for the owner to check for scheduled jobs in console
@commands.is_owner()
@bot.command(description="Dev command for checking job state in console")
async def checkjobs(ctx):
    print(scheduler.print_jobs())

# Define a command for the bot owner, or guild admins, to add channels where the bot will send out the message
@bot.command(description="Command for admins to add which channel the bot should send messages to", pass_context=True)
@is_admin_or_owner()
async def addchannel(ctx, channelid: str):
    current_guild = await bot.fetch_guild(ctx.guild.id)
    try:
        await current_guild.fetch_channel(channelid)
    except:
        await ctx.respond("Channel not in this server!")
        return
    c.execute(
        "INSERT OR IGNORE INTO channels (channel_id) VALUES (?)", (int(channelid),)
    )
    conn.commit()
    await ctx.respond(f"{channelid} has been added!")
    return
    
@addchannel.error
async def addchannel_error(ctx, error):
    if isinstance(error, discord.errors.CheckFailure):
        await ctx.respond("You must have admin perms to use this command!")
        return
    
# Define a command for the bot owner, or guild admins, to remove channels where the bot will send out the message
@bot.command(description="Command for admins to remove which channel the bot should send messages to", pass_context=True)
@is_admin_or_owner()
async def delchannel(ctx, channelid: str):
    current_guild = await bot.fetch_guild(ctx.guild.id)
    try:
        await current_guild.fetch_channel(channelid)
    except:
        await ctx.channel.send("Channel not in this server!")
        return
    c.execute(
        "DELETE FROM channels WHERE channel_id = ?", (int(channelid),)
    )
    conn.commit()
    await ctx.respond(f"{channelid} has been removed!")
    return
    
@delchannel.error
async def delchannel_error(ctx, error):
    if isinstance(error, discord.errors.CheckFailure):
        await ctx.respond("You must have admin perms to use this command!")
        return
    
# Defines a command for manually checking for free games
@bot.command(description="Check what the current free promotion is on Epic Games!")   
async def checkgames(ctx):
    promos = free.get_promos()
    cur = promos.get("current")
    if cur:
        embed = discord.Embed(
            title = "Free Game",
            description = cur[0],
            color = discord.Color.green()
        )
        embed.set_image(url=cur[1])
        await ctx.respond(embed=embed)

if __name__ == "__main__":
    bot.run(TOKEN)