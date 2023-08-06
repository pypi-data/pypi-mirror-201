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
import json
from pathlib import Path
import subprocess
import time
from typing import Dict, List

from karanage import KaranageConnection, KaranageState


def main():
    # Load arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", "--connection", type=str, help="json configuration file")
    parser.add_argument("-t", "--topic", type=str, help="Topic of the message")
    parser.add_argument(
        "-s", "--since", type=str, help="Iso date since the value time must be"
    )
    parser.add_argument(
        "-S", "--since-id", type=str, help="Remote BDD id to start request"
    )
    parser.add_argument(
        "-l", "--limit", type=int, default=100, help="Limit the number of request"
    )

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

    if args.topic is None:
        print("Missing TOPIC ...")
    else:
        data = stateInterface.get_history(
            topic=args.topic, since=args.since, since_id=args.since_id, limit=args.limit
        )
        tmp = []
        for elem in data:
            print(f"{elem.topic} @ {elem.time.astimezone()} =>  {elem.state}")
            print(json.dumps(elem.data, indent=4))

if __name__ == "__main__":
    main()