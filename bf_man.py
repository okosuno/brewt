import os
import yaml
from rich import print
from rich.prompt import Confirm

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
        'ingred': {'cactus': 16, 'sugar': 1}
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


def bf_exist():
    user_home = os.path.expanduser('~')
    try:
        if not os.path.exists(user_home + "/.config/brewt/brews.yaml"):
            if Confirm.ask(f"[red]brewt didn't find your brew file at [white]{user_home}/.config/brewt/brewt.yaml[/white]\nwould you like to create a default there now?"):
                if not os.path.exists(user_home + "/.config"):
                    os.mkdir(user_home + "/.config")
                    print(f"[green]created {user_home}/.config folder...")
                if not os.path.exists(user_home + "/.config/brewt"):
                    os.mkdir(user_home + "/.config/brewt")
                    print(f"[green]created {user_home}/.config/brewt folder...")
                with open(user_home + "/.config/brewt/brews.yaml", "w") as f:
                    yaml.safe_dump(BF_DEFAULT, f)
                    print(f"[green]created {user_home}/.config/brewt/brew.yaml file...")
    except Exception as e:
        print(f"[red]couldn't complete brewfile creation process\n{e}")
        quit()

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
        quit()
