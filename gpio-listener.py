#!/usr/bin/env python
#
# Listen for GPIO pins to be pressed, and call out to other scripts to do the
# work.
# 

import RPi.GPIO as GPIO
import time
import subprocess

PINLIST = [6, 13, 19, 26]
DISPATCH = {
  6 : lambda: TodoListPrinter("inbox"),
  13: lambda: RunExternal("echo bloop | lpr "),
}

def RunExternal(cmd):
  """Runs a command using subprocess."""
  #NB: this permits the use of shell interpretation, so dont take user input!
  # TODO: remove shell, check return values. etc.
  subprocess.call(cmd, shell=True)

def TodoListPrinter(query=None):
  """Calls the todoist script, using the included query string."""
  print "printing the thing: %s" % query


GPIO.setmode(GPIO.BCM)
for pin in DISPATCH.keys():
  GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
  for pin in DISPATCH.keys().sorted():
    input_state = GPIO.input(pin)
    # NB: "False" is ground. these pins are configured as pull-up.
    if input_state == False:
      DISPATCH[pin]()
      time.sleep(0.2)
    time.sleep(0.02)
