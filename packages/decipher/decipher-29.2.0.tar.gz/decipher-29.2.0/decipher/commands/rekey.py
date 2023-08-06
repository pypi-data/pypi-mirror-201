from __future__ import print_function
import sys
from decipher.beacon import BeaconAPIException


def rekey(api, args):
    ":type api: BeaconAPI"
    try:
        api._ensureKey()
        if api.keySource != 'ini':
            print ("Your beacon keys must be stored on the config file for this to be possible", file=sys.stderr)
            print ("Your current storage method is %r" % api.keySource, file=sys.stderr)
            return 1

        print("Rekeying...")
        api.rekey()

    except BeaconAPIException as e:
        print ("ERROR: %s" % e, file=sys.stderr)
    else:
        print("Complete. New secret key saved.")
