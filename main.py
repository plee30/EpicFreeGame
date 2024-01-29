import discord
import os
import schedule
import asyncio
from os.path import join, dirname
from dotenv import load_dotenv
import free

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
TOKEN = os.environ.get("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot()

def check_schedule():
    schedule.clear()
    promos = free.get_promos()
    cur = promos.get("current")
    fut = promos.get("future")
    if cur:
        print("testcur")
        pass
        # Function to send message in appropriate channel with cur information.
    if fut:
        # Function to schedule a check on the date and time of the next promotion
        add_future_task(fut[0], fut[1])
    else:
        # If no future, schedule for a week later
        pass

def add_future_task(day, when):
    match day:
        case 0:
            schedule.every().monday.at(when).do(check_schedule)
        case 1:
            schedule.every().tuesday.at(when).do(check_schedule)
        case 2:
            schedule.every().wednesday.at(when).do(check_schedule)
        case 3:
            schedule.every().thursday.at(when).do(check_schedule)
        case 4:
            schedule.every().friday.at(when).do(check_schedule)
        case 5:
            schedule.every().saturday.at(when).do(check_schedule)
        case 6:
            schedule.every().sunday.at(when).do(check_schedule)

    #print(cur, fut)
    # while True:
    #     schedule.run_pending()
    #     await asyncio.sleep(5)

# ##### Schedule Functions #####
# def schedule_task(datetime_to_execute):
#     # Schedule the task at the specified datetime
#     schedule.every().day.at(datetime_to_execute).do(freegames)

#     # Run the scheduler in a loop
#     while True:
#         print("test")
#         schedule.run_pending()
#         asyncio.sleep(1)

##### Bot functions ######
# Confirms bot is running
@bot.event
async def on_ready():
    # content = free.main()
    # print(content)
    print(f'We have logged in as {bot.user}')
    check_schedule()
    while True:
        schedule.run_pending()
        await asyncio.sleep(30)
    
# /create command
# Define a command to check for free games
@bot.command(description="Check for free games!")
async def freegames(ctx):
    content = free.main()
    print(content)
    next_promotion_datetime = "2024-01-26 14:25:15"
    embed = discord.Embed(
        title = "Free Game",
        description = content[0],
        color = discord.Color.green()
    )
    embed.set_image(url=content[1])
    print(next_promotion_datetime)
    #await ctx.respond(embed=embed)
    
# Define a command to check for scheduled jobs
@bot.command(description="Check for scheduled jobs!")
async def checkjobs(ctx):
    print(schedule.get_jobs())

if __name__ == "__main__":
    bot.run(TOKEN)
