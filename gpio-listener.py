#!/usr/bin/env python
#
# Listen for GPIO pins to be pressed, and call out to other scripts to do the
# work.
# 

import RPi.GPIO as GPIO
import time

PINLIST = [6, 13, 19, 26]
DISPATCH = {
  6 : lambda: TodoListPrinter("inbox")
}

def TodoListPrinter(query=None):
  """Calls the todoist script, using the included query string."""
  print "printing the thing: %s" % query


for pin in PINLIST:
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
  for pin in DISPATCH.keys().sorted()
    input_state = GPIO.input(pin)
    # NB: "False" is ground. these pins are configured as pull-up.
    if input_state == False:
      DISPATCH[pin]()
      time.sleep(0.2)
