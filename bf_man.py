import os, sys
import yaml
from pathlib import Path
from rich import print
from rich.prompt import Confirm, Prompt

BF_DEFAULT = {
    'lager_yeast': {
        'brew_time': 6,
        'age_time': None,
        'age_type': None,
        'distill': None,
        'ingred': {'pumpkin_seeds': 16, 'sugar': 1}
    },
    'tequila': {
        'brew_time': 10,
        'age_time': 2,
        'age_type': 'acacia',
        'distill': 2,
        'ingred': {'cactus': 16, 'wild yeast': 1}
    },
    'wild_yeast': {
        'brew_time': 7,
        'age_time': None,
        'age_type': None,
        'distill': None,
        'ingred': {'wheat_seeds': 16, 'sugar': 1}
    },
    'espresso': {
        'brew_time': 2,
        'age_time': None,
        'age_type': None,
        'distill': None,
        'ingred': {'acacia_leaves': 6}
    },
    'wheatbeer': {
        'brew_time': 4,
        'age_time': None,
        'age_type': 'any',
        'distill': None,
        'ingred': {'wheat': 6}
    },
    'pilsner': {
        'brew_time': 14,
        'age_time': 2,
        'age_type': 'oak',
        'distill': None,
        'ingred': {'wheat': 8, 'lager_yeast': 1, 'tall_grass': 2}
    },
    'red_wine': {
        'brew_time': 9,
        'age_time': 14,
        'age_type': 'spruce',
        'distill': None,
        'ingred': {'vines': 11}
    },
    'chardonnay': {
        'brew_time': 11,
        'age_time': 4,
        'age_type': 'oak',
        'distill': None,
        'ingred': {
            'vines': 11,
            'twisting_vines': 4,
            'brewers_yeast': 1,
            'oak_leaves': 4
        }
    },
    'cider': {
        'brew_time': 4,
        'age_time': 1,
        'age_type': 'any',
        'distill': None,
        'ingred': {'apples': 8}
    },
    'cherry_juice': {
        'brew_time': 2,
        'age_time': None,
        'age_type': None,
        'distill': None,
        'ingred': {'oak_leaves': 12, 'sugar': 3}
    },
    'whiskey': {
        'brew_time': 15,
        'age_time': 3,
        'age_type': 'any',
        'distill': 4,
        'ingred': {'wheat': 9, 'brewers_yeast': 1}
    },
    'potato_vodka': {
        'brew_time': 8,
        'age_time': None,
        'age_type': None,
        'distill': 3,
        'ingred': {'potatoes': 18, 'wild_yeast': 1}
    },
    'sake': {
        'brew_time': 18,
        'age_time': 3,
        'age_type': 'any',
        'distill': None,
        'ingred': {'seagrass': 15, 'wild_yeast': 1}
    },
    'kefir': {
        'brew_time': 10,
        'age_time': 3,
        'age_type': 'any',
        'distill': None,
        'ingred': {'milk_buckets': 6, 'wild_yeast': 1}
    },
    'earl_grey': {
        'brew_time': 6,
        'age_time': None,
        'age_type': None,
        'distill': None,
        'ingred': {'dark_oak_leaves': 12, 'peony': 1}
    },
    'vegetable_soup': {
        'brew_time': 25,
        'age_time': None,
        'age_type': None,
        'distill': None,
        'ingred': {'potatoes': 3, 'carrots': 3, 'beetroots': 2}
    },
    'zombie': {
        'brew_time': 1,
        'age_time': None,
        'age_type': None,
        'distill': None,
        'ingred': {'rum': 3, 'rotten_flesh': 2}
    }
}

CONFIG_DEFAULT = {
    'custom sound file name' : None,
    'timer mode': 'interval',
}

def file_handle(brewt_path = None):
    if brewt_path is None:
        brewt_path = os.path.expanduser('~') + "/.config/brewt"

    try:
        if os.path.exists(brewt_path + "/brews.yaml") == False or os.path.exists(brewt_path + "/config.yaml") == False:
            resp = Prompt.ask(f"[red]brewt didn't find files at [white]{brewt_path}[/white]\nwould you like for it to create default files there now?", 
            choices = ["yes","quit"] )
            if resp == "yes":
                if os.path.isdir(brewt_path) == False: os.mkdir(brewt_path)
                with open(brewt_path + "/brews.yaml", "w") as f:
                    yaml.safe_dump(BF_DEFAULT, f)
                    print(f"[green]created {brewt_path}/brews.yaml file...")
                with open(brewt_path + "/config.yaml", "w") as f:
                    yaml.safe_dump(CONFIG_DEFAULT, f)
                    print(f"[green]created {brewt_path}/config.yaml file...")
            elif resp == "quit":
                sys.exit(0)
    #except Exception as e:
    #    print(f"[red]couldn't complete file creation process\n{e}")
    #    sys.exit(0)
    except ValueError:
        pass

def validate_bf(brew_data):
    NoneType = type(None)

    cat_err = dict()
    type_err = dict()
    no_cat_err = dict()
    v_cat = set(['brew_time','age_time','age_type',"distill","ingred"])
    set_comp = set()

    for k, v in brew_data.items():
        if isinstance(brew_data[k],NoneType):
            no_cat_err[k] = f"no data entered for {k}."
            continue
        for i in v:
            set_comp.add(i)

        # too many keys
        comp_out = set_comp.difference(v_cat)
        if len(comp_out) > 0:
            cat_err[k] = f"bad category name: {comp_out}"

        # not enough keys
        comp_out = v_cat.difference(set_comp)
        if len(comp_out) > 0:
            cat_err[k] = f"missing category name: {comp_out}"
        set_comp.clear()

        for i in v_cat:
            if not isinstance(brew_data[k]['brew_time'],(int, float)):
                type_err[k] = f"incorrect type for 'brew_time'."
            if not isinstance(brew_data[k]['age_time'],(int, float, NoneType)):
                type_err[k] = f"incorrect type for 'age_time'."
            if not isinstance(brew_data[k]['age_type'],(str,NoneType)):
                type_err[k] = f"incorrect type for 'age_type'."
            if not isinstance(brew_data[k]['distill'],(int,NoneType)):
                type_err[k] = f"incorrect type for 'distill'."
            if not isinstance(brew_data[k]['ingred'],(dict)):
                type_err[k] = f"incorrect type for 'ingred'."

    if len(cat_err) or len(no_cat_err) or len(type_err):
        print(f"\n[red]errors found in [/red]brews.yaml[red]:")
        [ print(f"[red]{i}[/red] -> [orange]{v}[/orange]") for i, v in cat_err.items() ]
        [ print(f"[red]{i}[/red] -> [orange]{v}[/orange]") for i, v in no_cat_err.items() ]
        [ print(f"[red]{i}[/red] -> [orange]{v}[/orange]") for i, v in type_err.items() ]
        print("\n")
        sys.exit()

class Brewt_Config:
    def __init__(self, brewt_path) -> None:
        self.brewt_path = brewt_path
        with open(brewt_path + "/config.yaml", 'r') as f:
            self.config = yaml.safe_load(f)
        self.update_config()

    def update_config(self) -> None:
        self.sound_path = self.config['custom sound file name']
        self.timer_mode = self.config['timer mode']

    def change_config(self, sound_path = str, timer_mode = str, custom_path = str) -> None:
        conf_keys = self.config.keys()
        new_vals = ( sound_path, timer_mode, custom_path ) 
        self.config = dict(zip(conf_keys, new_vals))
        self.update_config()
        with open(self.brewt_path + "/config.yaml", 'w') as f:
            yaml.safe_dump(self.config, f)

