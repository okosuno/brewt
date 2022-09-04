# omokami's brew tool

#### this program:

- keeps track of all of your known brew recipes in a yaml file (my known brews provided)
- lets your quickly reference them within the program using a fuzzy search
- has a clean little cli with cute recipe cards
- creates concurrent timers using dbus notification system
- has time drift protection for accurate timekeeping

#### who is this for?

CivMC brewers but any brew mod users can use the basic template.  
the default provided yaml file just won't apply to you.

#### install

the most stable current version is on pip  
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

in game as omokami (ma suno & UTSS) or on the purple at okamime#9484
you're welcome to send me feature requests or berate me for poor choices!
also if you found this useful, feel free to send me recipes or hints!

#### appearance

[screenshots for your convenience.](https://imgur.com/a/AiGQmxc)
color scheme and font will depend on your terminal configuration.
