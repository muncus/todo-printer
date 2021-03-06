#!/usr/bin/env python
#
# Listen for GPIO pins to be pressed, and call out to other scripts to do the
# work.
# 

import RPi.GPIO as GPIO
import time
import subprocess

# in order of appearance on the board:
PINLIST = [26, 19, 13, 6 ]

DISPATCH = {
  26 : lambda: TodoListPrinter('p123'),
  19 : lambda: TodoListPrinter("inbox"),
}

def RunExternal(cmd):
  """Runs a command using subprocess."""
  #NB: this permits the use of shell interpretation, so dont take user input!
  # TODO: remove shell, check return values. etc.
  subprocess.call(cmd, shell=True)

def TodoListPrinter(query=None):
  """Calls the todoist script, using the included query string."""
  if not query:
    query = 'viewall'
  cmd_template = "/opt/todoprint/todolist.py -c /opt/todoprint/config.yml -q '{0}' | lpr"
  RunExternal(cmd_template.format(query))


GPIO.setmode(GPIO.BCM)
for pin in DISPATCH.keys():
  GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
  for pin in DISPATCH.keys():
    input_state = GPIO.input(pin)
    # NB: "False" is ground. these pins are configured as pull-up.
    if input_state == False:
      DISPATCH[pin]()
      time.sleep(0.3)
    time.sleep(0.02)
