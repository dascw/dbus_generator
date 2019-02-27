#!/usr/bin/env python2

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
parser = argparse.ArgumentParser(description='Battery')
parser.add_argument("-v", "--verbose", help="If the script should output logs",
                    action='store_true')
parser.add_argument("-n", "--name", help="the D-Bus service you want me to claim",
                    type=str, default="com.victronenergy.battery.socketcan_can0")
args = parser.parse_args()
# Init logging
logger = setup_logging(debug=args.verbose)
logger.info(__file__ + " is starting up, use -h argument to see optional arguments")

# Have a mainloop, so we can send/receive asynchronous calls to and from dbus
DBusGMainLoop(set_as_default=True)

pvac_output = DbusDummyService(
    servicename=args.name,
    productname='Battery',
    deviceinstance=233,
    paths={
        '/Alarms/CellImbalance': {'initial': 0, 'update': 0},
        '/Alarms/HighChargeCurrent': {'initial': 0, 'update': 0},
        '/Alarms/HighChargeTemperature': {'initial': 0, 'update': 0},
        '/Alarms/HighDischargeCurrent': {'initial': 0, 'update': 0},
        '/Alarms/HighTemperature': {'initial': 0, 'update': 0},
        '/Alarms/HighVoltage': {'initial': 0, 'update': 0},
        '/Alarms/InternalFailure': {'initial': 0, 'update': 0},
        '/Alarms/LowChargeTemperature': {'initial': 0, 'update': 0},
        '/Alarms/LowTemperature': {'initial': 0, 'update': 0},
        '/Alarms/LowVoltage': {'initial': 0, 'update': 0},
        '/Dc/0/Current': {'initial': -15, 'update': 0},
        '/Dc/0/Power': {'initial': -1000, 'update': 0},
        '/Dc/0/Temperature': {'initial': 30, 'update': 0},
        '/Dc/0/Voltage': {'initial': 50.5, 'update': 0},
        '/Info/BatteryLowVoltage': {'initial': 0, 'update': 0},
        '/Info/MaxChargeCurrent': {'initial': 50, 'update': 0},
        '/Info/MaxChargeVoltage': {'initial': 53.2, 'update': 0},
        '/Info/MaxDischargeCurrent': {'initial': 50, 'update': 0},
        '/Redetect': {'initial': 512, 'update': 0},
        '/Soc': {'initial': 50, 'update': 0},
        '/Soh': {'initial': 41, 'update': 0},
        })

print 'Connected to dbus, and switching over to gobject.MainLoop() (= event based)'
mainloop = gobject.MainLoop()
mainloop.run()
