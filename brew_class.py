import os, time, datetime, math, dbus, uuid, playsound, multiprocessing
from multiprocessing import Value

class Brew:

    def __init__(self, name, brew_data, countdown_int = 5, sound_path = ""):
        self.name = name
        self.id = int(uuid.uuid4().fields[0])
        self.brew_time = brew_data[self.name]["brew_time"]
        self.age_time = brew_data[self.name]["age_time"]
        self.age_type = brew_data[self.name]["age_type"]
        self.distill = brew_data[self.name]["distill"]
        self.ingred = brew_data[self.name]["ingred"]
        self.name = self.name.replace("_"," ")
        self.notif_code = self.name[0:3] + str(self.id)[-4:-1]
        self.countdown_int = countdown_int
        self.sound_path = sound_path
        # shared memory value for reporting to /t
        self.time_remaining = Value('i', 0)

    def notifier(self, summ, msg, acts, hints, exp_time) -> None:
        # notification system info https://dbus.freedesktop.org/doc/dbus-python/
        # https://specifications.freedesktop.org/notification-spec/notification-spec-latest.html
        item = "org.freedesktop.Notifications"
        notify_int = dbus.Interface(
            dbus.SessionBus().get_object(item, "/"+item.replace(".", "/")), item)
        notify_int.Notify("brewt", f"{self.id}", u"🍶", summ, msg, acts, hints, exp_time)

    def check_state(self, state) -> tuple:
        # state checks
        if state == "brew":
            total_time = self.brew_time * 60
            state_str = f"remaining for brewing."
            end_str = "now "
            if self.distill is not None:
                end_str = end_str + f"distill {self.distill} times, then "
            if self.age_time is not None:
                end_str = end_str + f"age {self.name} for {self.age_time} years in {self.age_type} wood barrel."
            else:
                end_str = f"brewing is now complete!"
        elif state == "age":
            total_time = self.age_time * 60 * 20
            state_str = f"remaining for aging."
            end_str = f"aging is now complete!"
        else:
            return (None, None)
        return (state_str, end_str, total_time)

    def notif_timer_constant(self, state, time_remaining) -> None:
        state_str, end_str, total_time = self.check_state(state)
            
        # countdown before starting brew
        time_remaining.value = total_time
        time_remaining_pre = 5
        for s in range(0, self.countdown_int):
            self.notifier(f"{self.name}", f"starting timer in {time_remaining_pre} seconds...", [], {"urgency": 1}, 0)
            time_remaining_pre = 5 - (s + 1)
        for s in range(0, total_time):
            # drift protection appropriated from https://codereview.stackexchange.com/questions/199743/countdown-timer-in-python
            target= datetime.datetime.now()
            one_second_later = datetime.timedelta(seconds=1)

            # format time remaining string
            if time_remaining.value >= 60:
                hours_str = ""
                days_str = ""
                minutes = math.floor(time_remaining.value/ 60)
                seconds= time_remaining.value % 60
                if minutes > 59: 
                    hours = math.floor(minutes / 60)
                    hours_str = f"{hours}h "
                    minutes = minutes % 60
                    if hours > 24:
                        days = math.floor(hours / 24)
                        days_str = f"{days}d "
                formatted_time = f"{days_str}{hours_str}{minutes}m {seconds}s"
            else:
                formatted_time = time_remaining.value

            # send notification each second  
            self.notifier(f"{self.name}", f"{formatted_time} {state_str}", [], {"urgency": 1}, 0)
            target += one_second_later
            time.sleep((target - datetime.datetime.now()).total_seconds())
            time_remaining.value = total_time - (s + 1)

        # end notification lives for one minute
        self.notifier(f"{self.name}", f"{end_str}", [], {"urgency": 1}, 60000)

        # play end sound
        if self.sound_path == "":
            print('\a', end="")
        else:
            playsound.playsound(self.sound_path)

    def notif_timer_interval(self, state, time_remaining):
        state_str, end_str, total_time = self.check_state(state)
        interval_times = ( total_time, round(total_time / 2), round(total_time / 4), 60, 30, 5)

        # countdown before starting brew
        time_remaining.value = total_time
        time_remaining_pre = 5
        for s in range(0, self.countdown_int):
            self.notifier(f"{self.name}", f"starting timer in {time_remaining_pre} seconds...", [], {"urgency": 1}, 0)
            time_remaining_pre = 5 - (s + 1)
        
        for s in range(0, total_time):
            # drift protection appropriated from https://codereview.stackexchange.com/questions/199743/countdown-timer-in-python
            target= datetime.datetime.now()
            one_second_later = datetime.timedelta(seconds=1)

            # format time remaining string
            if time_remaining.value >= 60:
                hours_str = ""
                days_str = ""
                minutes = math.floor(time_remaining.value/ 60)
                seconds= time_remaining.value % 60
                if minutes > 59: 
                    hours = math.floor(minutes / 60)
                    hours_str = f"{hours}h "
                    minutes = minutes % 60
                    if hours > 24:
                        days = math.floor(hours / 24)
                        days_str = f"{days}d "
                formatted_time = f"{days_str}{hours_str}{minutes}m {seconds}s"
            else:
                formatted_time = f"{time_remaining.value}s"

            # send notification for each interval 
            for interval in interval_times:
                if time_remaining.value == interval:
                    self.notifier(f"{self.name} ({self.notif_code})", f"{formatted_time} {state_str}", [], {"urgency": 1}, 10000)
            target += one_second_later
            time.sleep((target - datetime.datetime.now()).total_seconds())
            time_remaining.value = total_time - (s + 1)

        # end notification lives for one minute
        self.notifier(f"{self.name}", f"{end_str}", [], {"urgency": 1}, 60000)

        # play end sound
        if self.sound_path == "":
            print('\a', end="")
        else:
            playsound.playsound(self.sound_path)

        

    def start_timer(self, state, type) -> None:
        if type == "interval": tar = self.notif_timer_interval
        elif type == "constant": tar = self.notif_timer_constant
        else: raise Exception("no valid timer type with which to start timer. delete your config.yaml and start fresh.")

        self.timer = multiprocessing.Process(target=tar, args=(state, self.time_remaining))
        self.timer.start()
