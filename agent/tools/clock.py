import time
import threading
import datetime
import pytz

# alarms and timers storage
alarms = []
timers = []

def get_current_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%I:%M:%S %p')}"

def set_alarm(hour, minute, objective=""):
    def alarm_thread():
        while True:
            now = datetime.datetime.now()
            if now.hour == hour and now.minute == minute:
                print(f"Alarm: {objective or 'Wake up!'}")
                break
            time.sleep(10)

    threading.Thread(target=alarm_thread).start()
    alarms.append({"hour": hour, "minute": minute, "objective": objective})
    return f"Alarm set for {hour:02d}:{minute:02d} — {objective}"

def set_timer(seconds, objective=""):
    def timer_thread():
        time.sleep(seconds)
        print(f"⏳ Timer Done: {objective or 'Time is up!'}")

    threading.Thread(target=timer_thread).start()
    timers.append({"seconds": seconds, "objective": objective})
    return f"Timer set for {seconds} seconds — {objective}"

def clock(args: dict):
    cmd_type = args.get("type")

    if cmd_type == "get_time":
        return get_current_time()
    elif cmd_type == "alarm":
        return set_alarm(args.get("hour"), args.get("minute"), args.get("objective", ""))
    elif cmd_type == "timer":
        return set_timer(args.get("seconds"), args.get("objective", ""))
    elif cmd_type == "world_time":
        return get_time_in_timezone(args.get("city", ""))
    else:
        return "Unknown clock command."


