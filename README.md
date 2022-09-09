# omokami's brew tool

### a cute little cli tool for organizing and timing your brews!

#### this program:

- keeps track of all of your known brew recipes in a yaml file (my known brews provided)
- lets your quickly reference them within the program using a fuzzy search
- has a clean little cli with cute recipe cards
- creates concurrent timers using your notification system!
- has two modes: constant & interval
- has time drift protection for accurate timekeeping
- can play custom sounds on brew completion
- can take an argument if you want your config files somewhere specific
- is pretty cute!
- has currently only been tested on endeavourOS running i3wm. (lmk if it works on your system!)

#### who is this for?

CivMC brewers but any brew mod users can use the basic template.  
the default provided yaml file just won't apply to you.

#### install

you can grab the package off of github and do it the manual way.  
or, for your convenience, the most stable current version is on pip  
`pip install brewt`

#### usage

simply run the main files with an optional '-p' flag to specify a custom config path  
use the slash commands in the prompt to control the program  
every timer you start has a unique code attached to it   
this can be used to disambiguate batches you may have running at the same time   
it can also be used to kill specific timers using the "/k" command  

there are two timer modes because some notification systems will not update in place. they seem to ignore the "id" tag being passed in the notification, so the "constant" timer which ticks down every second will unfortunately flood users who have a notification system like this. if this happens to you, you will need to use the "interval" timer mode or see if you can tweak your notification systems configuration to be less janky.

#### planned features

- ~~slash commands to:~~ **done!**
    - ~~kill specific timers,~~ **done!**
    - ~~pretty print all recipe cards,~~ **done!**
    - ~~quit the program (currently ctrl+c)~~ **done!**
- ~~config file to:~~ **done!**
    - ~~turn on/off persistent notifications (only get a notif @ x time)~~ **done!**
    - ~~custom sounds~~ **done!**
- ~~allow custom brewfile location (currently ~/.config/brewt/brews.yaml)~~  **done!**
- set different sounds at different intervals
- custom countdown value

#### contact

in game as omokami (ma suno & UTSS) or on the purple at okamime#9484  
you're welcome to send me feature requests, bugs you run into,  or simply berate me for my poor choices!  
also if you found this useful, feel free to send me recipes or hints!

#### appearance

**warning, screenshots are from previous version of the program**
[screenshots for your convenience.](https://imgur.com/a/AiGQmxc)  
color scheme and font will depend on your terminal configuration.
