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
from typing import Any, Dict, List, Optional

from karanage import (
    KaranageConnection,
    KaranageException,
    KaranageState,
    StateSystem,
)
import psutil


cpu_core_count = psutil.cpu_count(logical=False)
cpu_thread_count = psutil.cpu_count()


def get_mounts() -> Dict:
    process = subprocess.Popen(
        ["mount", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    """get data format:
    $ mount -v
        proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
        sys on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
        dev on /dev type devtmpfs (rw,nosuid,relatime,size=7049156k,nr_inodes=1762289,mode=755,inode64)
        run on /run type tmpfs (rw,nosuid,nodev,relatime,mode=755,inode64)
        efivarfs on /sys/firmware/efi/efivars type efivarfs (rw,nosuid,nodev,noexec,relatime)
        /dev/nvme0n1p5 on / type ext4 (rw,relatime,stripe=32)
    """
    out = {}
    lines = stdout.decode("utf-8").split("\n")
    for line in lines:
        tmp = line.split(" ")
        if len(tmp) <= 2:
            continue
        if tmp[0].startswith("/dev/"):
            out[tmp[2]] = tmp[0][5:]
    return out


mounting_points = get_mounts()


def filter(data: Dict, filter_list: List[str]) -> Dict:
    out = {}
    # print(f"Request filter {data.keys()} with filter {filter_list}")
    for key in data:
        if key in filter_list:
            out[key] = data[key]
    return out


def need_process(data: Dict[str, Any]) -> Any:
    return data == "auto" or "include" in data


def create_cpu_data() -> Dict:
    # scpufreq(current=1605.5205625000003, min=400.0, max=4372.0)
    cpu_frequency = psutil.cpu_freq(percpu=False)
    cpu_percent_use = psutil.cpu_percent()
    return {
        "core": cpu_core_count,
        "thread": cpu_thread_count,
        "frequency": cpu_frequency.current,
        "use": cpu_percent_use,
        "max": cpu_frequency.max,
    }


def create_memory_data() -> Dict:
    # svmem(total=14473519104, available=8289726464, percent=42.7, used=5380497408, free=3276263424, active=1775763456, inactive=8335540224, buffers=361771008, cached=5454987264, shared=243720192, slab=544526336)
    mem = psutil.virtual_memory()
    return {
        "used": mem.used,
        "total": mem.total,
    }


def create_swap_data() -> Dict:
    # sswap(total=17179865088, used=262144, free=17179602944, percent=0.0, sin=0, sout=0)
    swap = psutil.swap_memory()
    return {
        "used": swap.used,
        "total": swap.total,
    }


def create_drive_data() -> Dict:
    tmp_elem = {}
    # nvme0n1p1 => sdiskio(read_count=187, write_count=3, read_bytes=6002176, write_bytes=5120, read_time=36, write_time=7, read_merged_count=504, write_merged_count=0, busy_time=67)
    drive_access = psutil.disk_io_counters(perdisk=True)
    for elem in mounting_points:
        # sdiskusage(total=255162540032, used=112077000704, free=130049380352, percent=46.3)
        drive_usage = psutil.disk_usage(elem)
        # print(f"plop {mounting_points[elem]} ==> {drive_access.keys()}")
        if mounting_points[elem] in drive_access:
            tmp_elem[elem] = {
                "read_bytes": drive_access[mounting_points[elem]].read_bytes,
                "write_bytes": drive_access[mounting_points[elem]].write_bytes,
                "used": drive_usage.used,
                "total": drive_usage.total,
            }
        else:
            tmp_elem[elem] = {
                "used": drive_usage.used,
                "total": drive_usage.total,
            }
    return tmp_elem


def create_network_data() -> Dict:
    # eth0 => snetio(bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0)
    data = psutil.net_io_counters(pernic=True)
    tmp_elem = {}
    for elem in data:
        tmp_elem[elem] = {
            "bytes_sent": data[elem].bytes_sent,
            "bytes_recv": data[elem].bytes_recv,
        }
    return tmp_elem


def agglutinate(configuration, name, data):
    if configuration[name] == "auto":
        return data
    elif "include" in configuration[name]:
        return filter(data, configuration[name]["include"])
    return none

def main():
    # Load arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="/etc/karanage/system.json",
        help="json configuration file",
    )
    parser.add_argument("-C", "--connection", type=str, help="json configuration file")

    # This element are read from the connection file:
    parser.add_argument("-u", "--url", type=str, help="Base URL of the web service")
    parser.add_argument("-g", "--group", type=str, help="Group the the message")
    parser.add_argument("-T", "--token", type=str, help="Token to access to the server")

    # This element are read from the configuration file:
    parser.add_argument(
        "-t", "--topic", type=str, default="PC/system", help="Topic of the message"
    )
    parser.add_argument(
        "-s", "--sleep", type=int, default=30, help="Periodicity of the messages"
    )
    parser.add_argument(
        "-d", "--display", help="Display the current state", action="store_true"
    )

    args = parser.parse_args()

    if Path(args.config).exists():
        f = open(args.config, "r")
        configuration = json.loads(f.read())
        f.close()
    else:
        configuration = {
            "cpu": "auto",
            "memory": "auto",
            "swap": "auto",
            "drive": "auto",
            "network": "auto",
        }
    # manage the configuration model
    if "config" not in configuration:
        configuration["config"] = {}
    if "display" not in configuration["config"]:
        configuration["config"]["display"] = args.display
    if "sleep" not in configuration["config"]:
        configuration["config"]["sleep"] = args.sleep
    if "topic" not in configuration["config"]:
        configuration["config"]["topic"] = args.topic

    connection = KaranageConnection(
        url=args.url, group=args.group, token=args.token, config_file=args.connection
    )

    # create the rest interface of karanage
    stateInterface = KaranageState(connection)

    while True:
        out = {}
        if need_process(configuration["cpu"]):
            base_elem = create_cpu_data()
            out["cpu"] = agglutinate(configuration, "cpu", base_elem)

        if need_process(configuration["memory"]):
            base_elem = create_memory_data()
            out["memory"] = agglutinate(configuration, "memory", base_elem)

        if need_process(configuration["swap"]):
            base_elem = create_swap_data()
            out["swap"] = agglutinate(configuration, "swap", base_elem)

        if need_process(configuration["drive"]):
            base_elem = create_drive_data()
            out["drive"] = agglutinate(configuration, "drive", base_elem)

        if configuration["network"] == "auto" or "include" in configuration["network"]:
            base_elem = create_network_data()
            out["network"] = agglutinate(configuration, "network", base_elem)
        # display of needed:
        if configuration["config"]["display"]:
            print(json.dumps(out, indent=4))
        # send message to the server:
        try:
            stateInterface.send(
                configuration["config"]["topic"], out, state=StateSystem.OK
            )
        except KaranageException as ex:
            print(f"Can not send to the server: {ex}")
        time.sleep(configuration["config"]["sleep"])

if __name__ == "__main__":
    main()