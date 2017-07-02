## Print my Todo List (from Todoist).

I like paper, but updating (and keeping track of) a paper todo list isn't easy.

So ive hooked up a thermal printer to a raspberry pi, and now i can print a new
list whenever i want!

## Build:

I used a [raspberry pi]() I had laying around, some buttons, and a [mini
thermal printer](https://www.adafruit.com/product/597).
The [networked thermal printer
tutorial](https://learn.adafruit.com/networked-thermal-printer-using-cups-and-raspberry-pi)
is solid, and helped me get the printer up and running.

The [Pi pinout](https://pinout.xyz/) outlines the "software names" of the pins
on the pi. I chose to put some buttons in the section opposite the pins used
for the printer (near BCM pin 26), because of their easy access to a Ground
pin.

## Todolist.py Usage:

This script requires that the python todoist api client be installed:

`pip install todoist-python`

`todolist.py` can be run with either `--token` or `--config` options to provide a todoist api token.

To use `--config`, provide a valid yaml file like the following:

`token: YOURTOKENGOESHERE`

For help with tokens, see the [ToDoist developer
site](https://developer.todoist.com/index.html#authorization)

The script also takes a `--query` option. Unfortunately, for Free users like me,
the queries accepted are extremely limited, and dont support most of the filter
operations. The following seem to work: `viewall`, `overdue`, `p1`, `no date`.

`todolist.py -c config.yml -q 'viewall'`

## GPIO Listener

The included script `gpio_listener.py` can be used to take actions based on
inputs on the Pi's GPIO pins (e.g. pressing a physical button). The script
itself is pretty basic, but should be configurable enough for reuse in other
projects.

The `debian/` folder contains the necessary configuration to build a debian
package which will run the GPIO Listener as a service, via systemd.

## Future work
* templates for todolist output, prettier output.
