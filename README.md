# omokami's brew tool

#### this program:

- keeps track of all of your known brew recipes in a yaml file (my known brews provided)
- lets your quickly reference them within the program using a fuzzy search
- creates concurrent timers using dbus notification system
- has a clean little cli menu which doesn't look obnoxious
- has drift protection for accurate timekeeping

#### who is this for?

CivMC brewers but any brew mod users can use the basic template.  
the default provided yaml file just won't apply to you.

#### install

it's on pip
`pip install brewt`

#### planned features

- slash commands to:
    - ~~kill specific timers,~~ **done!**
    - ~~pretty print all recipe cards,~~ **done!**
    - ~~quit the program (currently ctrl+c)~~ **done!**
- config file to:
    - turn on/off persistent notifications (only get a notif @ x time)
    - custom sounds at different x seconds remaining
    - custom brewfile location (currently ~/.config/brewt/brews.yaml)

#### contact

in game as omokami or on the purple at okamime#9484
feel free to send me recipes or hints! what you see here is what i have.
