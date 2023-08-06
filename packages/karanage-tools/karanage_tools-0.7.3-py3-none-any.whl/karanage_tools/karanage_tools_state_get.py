#!/usr/bin/python3
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2023, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##
import argparse
from datetime import timezone
import json
from pathlib import Path
import subprocess
import time
from typing import Dict, List

from karanage import (
    KaranageConnection,
    KaranageException,
    KaranageState,
)


def main():
    # Load arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", "--connection", type=str, help="json configuration file")
    parser.add_argument("-t", "--topic", type=str, help="Topic of the message")
    parser.add_argument(
        "-s", "--since", type=str, help="Iso date since the value time must be"
    )
    parser.add_argument("-w", "--watch", help="Display new states", action="store_true")

    # This element are read from the connection file:
    parser.add_argument("-u", "--url", type=str, help="Base URL of the web service")
    parser.add_argument("-g", "--group", type=str, help="Group the the message")
    parser.add_argument("-T", "--token", type=str, help="Token to access to the server")

    args = parser.parse_args()

    connection = KaranageConnection(
        url=args.url, group=args.group, token=args.token, config_file=args.connection
    )

    # create the rest interface of karanage
    stateInterface = KaranageState(connection)

    # transform since in a datetime:
    while True:
        if args.topic is not None:
            elem = stateInterface.get(topic=args.topic, since=args.since)
            if elem is not None:
                print(f"{elem.topic} @ {elem.time.astimezone()} =>  {elem.state}")
                print(json.dumps(elem.data, indent=4))
                args.since = elem.time
        else:
            data = stateInterface.gets(since=args.since)
            for elem in data:
                print(f"{elem.topic} @ {elem.time.astimezone()} =>  {elem.state}")
                print(json.dumps(elem.data, indent=4))
                args.since = elem.time
        if not args.watch:
            break
        else:
            time.sleep(1)

if __name__ == "__main__":
    main()