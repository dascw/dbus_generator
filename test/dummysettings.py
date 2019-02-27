#!/usr/bin/env python

from dbus.mainloop.glib import DBusGMainLoop
import gobject
import argparse
import sys
import os

# our own packages
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../ext/velib_python'))
from dbusdummyservice import DbusDummyService
from logger import setup_logging

# Argument parsing
parser = argparse.ArgumentParser(description='Setting')
parser.add_argument("-v", "--verbose", help="If the script should output logs",
                    action='store_true')
parser.add_argument("-n", "--name", help="the D-Bus service you want me to claim",
                    type=str, default="com.victronenergy.settings")
args = parser.parse_args()
# Init logging
logger = setup_logging(debug=args.verbose)
logger.info(__file__ + " is starting up, use -h argument to see optional arguments")

# Have a mainloop, so we can send/receive asynchronous calls to and from dbus
DBusGMainLoop(set_as_default=True)

pvac_output = DbusDummyService(
    servicename=args.name,
    deviceinstance=3,
    productname='Settings',
    paths={
        '/Settings/CGwacs/BatteryLife/State': {'initial': 2, 'update': 0},
        '/Settings/CGwacs/BatteryLife/SocLimit': {'initial': 15, 'update': 0},
        '/Settings/CGwacs/BatteryLife/MinimumSocLimit': {'initial': 10, 'update': 0},
        '/Settings/CGwacs/AcPowerSetPoint': {'initial': 50, 'update': 0},
        '/Settings/CGwacs/Hub4Mode': {'initial': 3, 'update': 0}
    })

logger.info('Connected to dbus, and switching over to gobject.MainLoop() (= event based)')
mainloop = gobject.MainLoop()
mainloop.run()
