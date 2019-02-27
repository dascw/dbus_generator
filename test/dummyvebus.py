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
parser = argparse.ArgumentParser(description='VeBus')
parser.add_argument("-v", "--verbose", help="If the script should output logs",
                    action='store_true')
parser.add_argument("-n", "--name", help="the D-Bus service you want me to claim",
                    type=str, default="com.victronenergy.vebus.ttyS3")
args = parser.parse_args()
# Init logging
logger = setup_logging(debug=args.verbose)
logger.info(__file__ + " is starting up, use -h argument to see optional arguments")

# Have a mainloop, so we can send/receive asynchronous calls to and from dbus
DBusGMainLoop(set_as_default=True)

pvac_output = DbusDummyService(
    servicename=args.name,
    deviceinstance=231,
    productname='Multi',
    paths={
        '/Hub4/L1/CurrentLimitedDueToHighTemp': {'initial': 0, 'update': 0},
        '/Hub4/Sustain': {'initial': 0, 'update': 0},
        '/Hub4/DisableCharge': {'initial': 0, 'update': 0},
        '/Hub4/DisableFeedIn': {'initial': 1, 'update': 0},
        '/Ac/ActiveIn/CurrentLimit': {'initial': 32, 'update': 0},
        '/Ac/ActiveIn/L1/F': {'initial': 50.1026, 'update': 0},
        '/Ac/ActiveIn/L1/I': {'initial': 7.41, 'update': 0},
        '/Ac/ActiveIn/L1/P': {'initial': 1754, 'update': 0},
        '/Ac/ActiveIn/L1/S': {'initial': -2486, 'update': 0},
        '/Ac/Out/L1/F': {'initial': 49.8214, 'update': 0},
        '/Ac/Out/L1/I': {'initial': -0.25, 'update': 0},
        '/Ac/Out/L1/P': {'initial': -21, 'update': 0},
        '/Ac/Out/L1/S': {'initial': 107, 'update': 0},
        '/Dc/0/Current': {'initial': 31.2, 'update': 0},
        '/Dc/0/Voltage': {'initial': 50.7, 'update': 0},
        '/Dc/0/Power': {'initial': 1783, 'update': 0},
        '/Energy/AcIn1ToAcOut': {'initial': 0, 'update': 0},
        '/Energy/AcIn1ToInverter': {'initial': 2.33, 'update': 0},
        '/Energy/AcIn2ToAcOut': {'initial': 0, 'update': 0},
        '/Energy/AcIn2ToInverter': {'initial': 0, 'update': 0},
        '/Energy/AcOutToAcIn1': {'initial': 0, 'update': 0},
        '/Energy/AcOutToAcIn2': {'initial': 0, 'update': 0},
        '/Energy/InverterToAcIn1': {'initial': 1.20149, 'update': 0},
        '/Energy/InverterToAcIn2': {'initial': 0, 'update': 0},
        '/Energy/InverterToAcOut': {'initial': 0.0364089, 'update': 0},
        '/Alarms/L1/HighTemperature': {'initial': 0, 'update': 0},
        '/Alarms/L1/LowBattery': {'initial': 0, 'update': 0},
        '/Alarms/L1/Overload': {'initial': 0, 'update': 0},
        '/Soc': {'initial': 50, 'update': 0},
        '/State': {'initial': 3, 'update': 0},
        '/Devices/0/Version': {'initial': 2628453, 'update': 0}}
    )

logger.info('Connected to dbus, and switching over to gobject.MainLoop() (= event based)')
mainloop = gobject.MainLoop()
mainloop.run()
