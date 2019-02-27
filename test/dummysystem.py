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
parser = argparse.ArgumentParser(description='System')
parser.add_argument("-v", "--verbose", help="If the script should output logs",
                    action='store_true')
parser.add_argument("-n", "--name", help="the D-Bus service you want me to claim",
                    type=str, default="com.victronenergy.system")
args = parser.parse_args()
# Init logging
logger = setup_logging(debug=args.verbose)
logger.info(__file__ + " is starting up, use -h argument to see optional arguments")

# Have a mainloop, so we can send/receive asynchronous calls to and from dbus
DBusGMainLoop(set_as_default=True)

pvac_output = DbusDummyService(
    servicename=args.name,
    deviceinstance=230,
    productname='Settings',
    paths={
        '/Ac/Consumption/L1/Power': {'initial': 13, 'update': 0},
        '/Ac/Grid/L1/Power': {'initial': 1100, 'update': 0},
        '/Ac/PvOnGrid/L1/Power': {'initial': 0, 'update': 0},
        '/Dc/Battery/Voltage': {'initial': 49.5, 'update': 0},
        '/Dc/Battery/Current': {'initial': 20.2, 'update': 0},
        '/Dc/Battery/Power': {'initial': 1015, 'update': 0},
        '/Dc/Battery/Soc': {'initial': 22, 'update': 0},
        '/Dc/Battery/Temperature': {'initial': 39.1, 'update': 0},
        '/Dc/Battery/State': {'initial': 1, 'update': 0}
    })

logger.info('Connected to dbus, and switching over to gobject.MainLoop() (= event based)')
mainloop = gobject.MainLoop()
mainloop.run()
