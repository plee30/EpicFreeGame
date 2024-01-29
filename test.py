import schedule
import time
from datetime import datetime, timedelta
# days = {
#     0: "monday",
#     1: "tuesday",
#     2: "wednesday",
#     3: "thursday",
#     4: "friday",
#     5: "saturday",
#     6: "sunday"
# }
def sched(tday, sched_datetime):
    match tday:
        case 0:
            schedule.every().monday.at(sched_datetime).do(my_task, tday)
        case 1:
            schedule.every().tuesday.at(sched_datetime).do(my_task, tday)
        case 2:
            schedule.every().wednesday.at(sched_datetime).do(my_task, tday)
        case 3:
            schedule.every().thursday.at(sched_datetime).do(my_task, tday)
        case 4:
            schedule.every().friday.at(sched_datetime).do(my_task, tday)
        case 5:
            schedule.every().saturday.at(sched_datetime).do(my_task, tday)
        case 6:
            schedule.every().sunday.at(sched_datetime).do(my_task, tday)


def my_task(tday):
    # Calling the timedelta() function  
    curtime = datetime.now() + timedelta(seconds=3)
    scheduled_datetime = curtime.strftime("%H:%M:%S")
    sched(tday, scheduled_datetime)
    # # Schedule the task to run at the specified datetime
    # schedule.every().day.at(scheduled_datetime.strftime("%H:%M:%S")).do(my_task)
    print("Executing my task at:", time.ctime())

if __name__ == "__main__":
    # Specify the date and time for the task to run
    curtime = datetime.now() + timedelta(seconds=5)
    # scheduled_datetime = curtime.strftime("%d-%m-%Y %H:%M:%S") 
    scheduled_datetime = curtime.strftime("%H:%M:%S") 
    print(scheduled_datetime)
    tday = datetime.today().weekday()
    print(tday)
    sched(tday, scheduled_datetime)
#scheduled_datetime_str = "2024-01-26 16:08:20"  # Replace with your desired datetime
#scheduled_datetime = datetime.strptime(scheduled_datetime_str, "%Y-%m-%d %H:%M:%S")
# schedule.every().day.at(scheduled_datetime.strftime("%H:%M:%S")).do(my_task)
    # Run the scheduler in a loop
    while True:
        schedule.run_pending()
        time.sleep(1)
