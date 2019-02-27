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
parser = argparse.ArgumentParser(description='Meters')
parser.add_argument("-v", "--verbose", help="If the script should output logs",
                    action='store_true')
parser.add_argument("-n", "--name", help="the D-Bus service you want me to claim",
                    type=str, default="com.victronenergy.grid.cgwacs_ttyUSB2_di30_mb1")
args = parser.parse_args()
# Init logging
logger = setup_logging(debug=args.verbose)
logger.info(__file__ + " is starting up, use -h argument to see optional arguments")
# Have a mainloop, so we can send/receive asynchronous calls to and from dbus
DBusGMainLoop(set_as_default=True)

pvac_output = DbusDummyService(
    servicename=args.name,
    deviceinstance=222,
    productname='Meters',
    paths={
        '/Ac/Current': {'initial': 0, 'update': 0},
        '/Ac/Voltage': {'initial': 0, 'update': 0},
        '/Ac/Power': {'initial': 0, 'update': 0},
        '/Ac/L1/Current': {'initial': 0, 'update': 0},
        '/Ac/L1/Voltage': {'initial': 0, 'update': 0},
        '/Ac/L1/Power': {'initial': 0, 'update': 0},
        '/Ac/L2/Current': {'initial': 0, 'update': 0},
        '/Ac/L2/Voltage': {'initial': 0, 'update': 0},
        '/Ac/L2/Power': {'initial': 0, 'update': 0},
        '/Ac/Energy/Forward': {'initial': 0, 'update': 0},
        '/Ac/Energy/Reverse': {'initial': 0, 'update': 0}}
    )

logger.info('Connected to dbus, and switching over to gobject.MainLoop() (= event based)')
mainloop = gobject.MainLoop()
mainloop.run()
