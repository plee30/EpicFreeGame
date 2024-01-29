import discord
import os
from os.path import join, dirname
from dotenv import load_dotenv
import free
from apscheduler.schedulers.asyncio import AsyncIOScheduler

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
TOKEN = os.environ.get("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot()
scheduler = AsyncIOScheduler()
scheduler.start()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await check_schedule()

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
    
async def add_future_task(future_promo_datetime):
    scheduler.add_job(check_schedule, 'date', run_date=future_promo_datetime)
    
async def freegames_auto(cur):
    # TODO Change from hard-implementation of channel ID to database of channels to send to
    channel = bot.get_channel()
    embed = discord.Embed(
        title = "Free Game",
        description = cur[0],
        color = discord.Color.green()
    )
    embed.set_image(url=cur[1])
    await channel.send(embed=embed)

# Define a command to check for scheduled jobs
@bot.command(description="Dev command for checking job state in console")
async def checkjobs(ctx):
    print(scheduler.print_jobs())

if __name__ == "__main__":
    bot.run(TOKEN)