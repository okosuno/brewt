#!/usr/bin/env python3
import os, sys
import yaml
import rapidfuzz
import argparse

from brew_class import Brew
from bf_man import *

from rich import print
from rich import box
from rich.prompt import Prompt, Confirm
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

aparser = argparse.ArgumentParser()
aparser.add_argument("-p", "--path", help="specify a location for brewt's files", default=f"{os.path.expanduser('~') + '/.config/brewt'}")
args = aparser.parse_args()

# file ops

file_handle(args.path)
with open(args.path + "/brews.yaml", 'r') as f:
    BREW_DATA = yaml.safe_load(f)
validate_bf(BREW_DATA)
BREW_DATA_KEYS = sorted(BREW_DATA.keys())
brewt_config_file = Brewt_Config(args.path)

def main():

    print(pretty_recipe_list())

    print(f"[yellow][bold]omokami's brewtool[/bold][/yellow]\n"
    f"[green]your configs are at [/green][white]{args.path}[/white]\n"
    f"[green]your timer mode is set to [white]{brewt_config_file.timer_mode}[white].[/green]\n\n",
    f"[green]type 'q' start over.\n\n",
    f"[yellow bold]slash commands:[/yellow bold]\n",
    f"[yellow]kill active timer [white](/k timer_id)\n",
    f"[yellow]list timer ids [white](/t)\n",
    f"[yellow]pretty print all recipe cards [white](/p)\n",
    f"[yellow]change timer mode [white](/ch interval/constant)\n",
    f"[yellow]specify a custom finish sound [white](/sp sound_path)\n",
    f"[yellow]exit program [white](/q)[/white]\n\n")

    menu_loop()

def pretty_recipe_list():

    pretty_keys = []
    for i in BREW_DATA_KEYS:
        pretty_keys.append(f"[green]{i.replace('_',' ')}[/green]")
    columns = Columns(pretty_keys,equal=True, expand=True, padding=(1,1), title="[bold yellow]brew file[/bold yellow]\n", align="center")
   
    return Panel(Panel(columns,width=75, padding=(1,2,1,2)), expand=False, box=box.MINIMAL)

def pretty_brew_card(brew_obj: Brew):
    
    card = list()
    card.append(f"[blue]ingredients:[/blue]")

    for i, q in brew_obj.ingred.items():
        card.append(f"[green]{q} {i.replace('_',' ')}[/green]")

    card.append("")
    card.append(f"[blue]brew for [/blue][white]{brew_obj.brew_time}[/white] [blue]minutes.[/blue]")

    if brew_obj.distill != None:
        card.append(f"[blue]distill [white]{brew_obj.distill}[/white] times.[/blue]")
    if brew_obj.age_time != None:
        card.append(f"[blue]age for [/blue][white]{brew_obj.age_time} [blue]years.[/blue]")

    card_table = Table(title=f"[yellow bold]{brew_obj.name.replace('_',' ')}[/yellow bold]", box=None)

    for i in card:
            card_table.add_row(i)

    return Panel(Panel(card_table, padding=(1,1,1,1)), expand=False, padding=(0,0,0,0), box=box.MINIMAL)

def pretty_card_list():

    every_brew_obj = []
    for i in BREW_DATA_KEYS:
        every_brew_obj.append(pretty_brew_card(Brew(i,BREW_DATA)))
    columns = Columns(every_brew_obj,equal=True, expand=True, padding=(1,1), title="[bold yellow]brew file[/bold yellow]\n", align="center")
   
    return Panel(Panel(columns, padding=(1,2,1,2)), expand=True, box=box.MINIMAL)

def menu_loop():
    running_timers = dict()    
    
    try:
        while True:
            running_timers = timer_cleaner(running_timers)

            # input handling
            brew_name = Prompt.ask("[yellow]brew name")
            if len(brew_name) == 0: continue
            if brew_name[0] == "/": 
                running_timers = slash_handle(brew_name,running_timers)
                continue
            if brew_name == "q": 
                continue

            # create brew objects if they match a config entry
            validated_brew = name_check(brew_name)
            if isinstance(validated_brew, str):
                new_brew = Brew(validated_brew, BREW_DATA, sound_path = brewt_config_file.sound_path)
                print()
            else: continue
            print(pretty_brew_card(new_brew))

            # confirm selection
            validate = Confirm.ask(f"[green]confirm [bold]{new_brew.name}[/bold]?",default="y")
            if not validate: continue

            # make calculations and add timers
            if new_brew.age_time != None:
                state = Prompt.ask("[yellow]state", choices=["b","brew","brewing","a","age","aging","q"], show_choices=False)
                if state == "q":
                    print("\n")
                    continue
                elif state == "b" or state =="brew" or state == "brewing":
                    state = "brew"
                else: 
                    state = "age"
            else:
                state = "brew"

            new_brew.start_timer(state, brewt_config_file.timer_mode)
            print(f"[yellow]brew created ([white]{new_brew.notif_code}[/white])")
            running_timers[new_brew.notif_code] = new_brew

    except KeyboardInterrupt:
        print("\n")
        sys.exit(0)

def slash_handle(query, running_timers):
    running_timers = timer_cleaner(running_timers)
    command = query[1:]
    
    if command[0] == "p":
        print(pretty_card_list())

    # kills a thread and pops it out of the active threads list
    elif command[0:2] == "k ":
        notif_code = command[2:len(command)]
        try:
            running_timers[notif_code].timer.terminate()
            running_timers.pop(notif_code)
        except KeyError:
            print(f"[white]{notif_code}[red] doesn't match any timers!")
            return running_timers
        print(f"[green]successfully terminated [white]{notif_code}")

    # lists all tids of running timers
    elif command[0] == "t":
        timer_data = set()
        for i in running_timers.values():
            if i.time_remaining.value != 0:
                timer_data.add(f"[green]{i.notif_code} has [white]{i.time_remaining.value}[/white] seconds left")
        if timer_data == set():
            print("[yellow bold]no timers currently active...")
        else:
            [ print(i) for i in timer_data ]
            timer_data.clear()

    # terminate all threads and then quit the program
    elif command[0] == "q":
        if running_timers is not None and len(running_timers) > 0:
            [ (i.timer.terminate(),print(f"[white]{i.notif_code}[/white][red] was terminated.")) for i in running_timers.values() ]
        os._exit(0)
    
    # change timer type
    elif command[0:3] == "ch ":
        new_val = command[3:len(command)]
        if new_val == "interval" or new_val == "constant":
            brewt_config_file.change_config(timer_mode = new_val)
            brewt_config_file.update_config()
            print(f"[green]updated config.yaml!")
        else: print(f"[red]invalid command!")

    # custom sound path
    elif command[0:3] == "sp ":
        new_val = command[3:len(command)]
        if os.path.exists(new_val):
            brewt_config_file.change_config(sound_path=new_val)
            brewt_config_file.update_config()
            print(f"[green]updated sound file!")
        else: print(f"[red]path {new_val} doesn't exist!")
    
    else:
        print(f"/{command} doesn't match any commands.")

    return running_timers

def name_check(name):
    # fuzzy matching for brew names
    name_search = rapidfuzz.process.extract(name, BREW_DATA_KEYS, limit=1)
    if name_search[0][1] < 50:
        print("no adequate match found for that brew...")
        return 0
    else:
        return name_search[0][0]

def timer_cleaner(running_timers):
    # check for done brews, use copy to avoid RunTimeError
    for k, v in running_timers.copy().items():
        if v.time_remaining.value < 1:
            print('{k} timer vacated with {v.time_remaining.value} seconds left')
            running_timers.pop(k)
    return running_timers

if __name__ == "__main__":
    main()
