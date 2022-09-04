#!/usr/bin/env python3
import os, sys
import yaml
import rapidfuzz

from brewt.brew_class import Brew
from brewt.bf_man import validate_bf, bf_exist

from rich import print
from rich import box
from rich.prompt import Prompt, Confirm
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

# file ops
bf_exist()
USER_HOME = os.path.expanduser( '~' )
with open(USER_HOME + '/.config/brewt/brews.yaml', 'r') as f:
    BREW_DATA = yaml.safe_load(f)
validate_bf(BREW_DATA)
BREW_DATA_KEYS = sorted(BREW_DATA.keys())

def main():

    print(pretty_recipe_list())

    print(f"[yellow][bold]omokami's brewtool[/bold][/yellow]\n"
    f"[green]your config file is located at [/green][white]{USER_HOME}/.config/brewt/brews.yaml[/white]\n"
    f"[green]type 'q' to start over.\n\n"
    f"[yellow bold]slash commands:[/yellow bold][yellow]\nkill active timer\n[white]/k (timer id)[/white]\nlist timer ids\n[white]/t[/white]\npretty print all recipe cards\n[white]/p[/white]\nexit program\n[white]/q[/white]\n\n")
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
            brew_name = Prompt.ask("[yellow]brew name")
            if len(brew_name) == 0: continue
            if brew_name[0] == "/": 
                slash_handle(brew_name,running_timers)
                continue
            if brew_name == "q": 
                continue
            validated_brew = name_check(brew_name)
            if isinstance(validated_brew, str):
                new_brew = Brew(validated_brew, BREW_DATA)
                print()
            else: continue

            print(pretty_brew_card(new_brew))

            validate = Confirm.ask(f"[green]confirm [bold]{new_brew.name}[/bold]?",default="y")
            if not validate: continue

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

            new_brew.start_timer(state)
            print(f"[yellow]brew created ([white]{new_brew.notif_code}[/white])")
            running_timers[new_brew.notif_code] = new_brew

    except KeyboardInterrupt:
        print("\n")
        quit()

def slash_handle(query, running_timers):
    command = query[1:]
    
    if command[0] == "p":
        print(pretty_card_list())
        return

    if command[0] == "k":
        notif_code = query[2:]
        try:
            running_timers[notif_code].timer.terminate()
        except KeyError:
            print(f"[white]{notif_code}[red] doesn't match any timers!")
            return
        print(f"[green]successfully terminated [white]{notif_code}")

    if command[0] == "t":
        print("[green]running timer codes:")
        [ print(f"[green]{i.notif_code} has [white]{i.time_remaining.value}[/white] seconds left") for i in running_timers.values() ]
        return

    if command[0] == "q":
        sys.exit(0)

    else:
        print(f"/{command[0]} doesn't match any current commands.")

def name_check(name):
    name_search = rapidfuzz.process.extract(name, BREW_DATA_KEYS, limit=1)
    if name_search[0][1] < 50:
        print("no adequate match found for that brew...")
        return 0
    else:
        return name_search[0][0]

if __name__ == "__main__":
    main()
