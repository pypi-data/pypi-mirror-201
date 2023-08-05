#!/usr/bin/python
# Copyright (C) 2016 Red Hat, Inc.
# This file is part of libsan.
#
# libsan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# libsan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with libsan.  If not, see <http://www.gnu.org/licenses/>.

"""
Tool to perform basic commands on SAN
"""

import argparse
import json
import sys

import libsan.host.dt
import libsan.host.fcoe
import libsan.host.fio
import libsan.host.linux
import libsan.host.lio
import libsan.host.net
import libsan.host.scsi
import libsan.sanmgmt
from libsan.misc.time import get_time, time_2_sec

OBJ_SANMGMT = None


def _show_san_conf():
    """
    Show SAN config file
    """
    san_conf = libsan.sanmgmt.load_san_conf()
    print(json.dumps(san_conf, indent=4))


def _show_host_cfg():
    """
    Show SAN configuration of the host
    """
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    nics = libsan.host.net.get_nics()
    macs = []
    if nics:
        for nic in nics:
            macs.append(libsan.host.net.get_mac_of_nic(nic))
    if macs:
        print("Host has the following MACs:")
        for mac in macs:
            sw_port = "Not configured on SAN top"
            connected_sw = OBJ_SANMGMT.get_sw_self(mac)
            if connected_sw:
                sw_port = connected_sw["port_of"][mac]
            print(f"\t{mac} - SW port: {sw_port}")

    iscsi_macs = OBJ_SANMGMT.macs()
    if iscsi_macs:
        print("Host has the following iSCSI MACs:")
        for mac in iscsi_macs:
            sw_port = "Not configured on SAN top"
            connected_sw = OBJ_SANMGMT.get_sw_self(mac)
            if connected_sw:
                sw_port = connected_sw["port_of"][mac]
            print(f"\t{mac} - SW port: {sw_port}")

    h_wwpns = OBJ_SANMGMT.h_wwpns()
    if h_wwpns:
        print("Host has the following h_wwpns configured:")
        for wwpn in h_wwpns:
            sw_port = "Not configured on SAN top"
            connected_sw = OBJ_SANMGMT.get_sw_self(wwpn)
            if connected_sw:
                sw_port = connected_sw["port_of"][wwpn]
            print(f"\t{wwpn} - SW port: {sw_port}")

    t_wwpns = OBJ_SANMGMT.t_wwpns()
    if t_wwpns:
        print("Host has the following t_wwpns configured:")
        for wwpn in t_wwpns:
            connected_sw = OBJ_SANMGMT.get_sw_self(wwpn)
            if connected_sw:
                sw_port = connected_sw["port_of"][wwpn]
                print(f"\t{wwpn} - SW port: {sw_port}")


def _check_ports_ready():
    """
    Check if all ports need for test are up
    """
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)
    return OBJ_SANMGMT.check_ports_ready()


def _rcsn_enable(port_addr):
    """
    Enable RCSN
    """
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    if not port_addr:
        print("FAIL: rcsn_enable() - requires port_addr as parameter")
        return False

    connected_sw = OBJ_SANMGMT.get_sw_self(port_addr)
    if not connected_sw:
        print("FAIL: %s is not managed by libsan" % port_addr)
        return False
    return OBJ_SANMGMT.rcsn_enable(addr=port_addr)


def _rcsn_disable(port_addr):
    """
    Disable RCSN
    """
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    if not port_addr:
        print("FAIL: rcsn_disable() - requires port_addr as parameter")
        return False

    connected_sw = OBJ_SANMGMT.get_sw_self(port_addr)
    if not connected_sw:
        print("FAIL: %s is not managed by libsan" % port_addr)
        return False
    return OBJ_SANMGMT.rcsn_disable(addr=port_addr)


def _port_disconnect(port_addr):
    """
    Disable switch port
    """
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    if not port_addr:
        print("FAIL: port_disconnect() - requires port_addr as parameter")
        return False

    connected_sw = OBJ_SANMGMT.get_sw_self(port_addr)
    if not connected_sw:
        print("FAIL: %s is not managed by libsan" % port_addr)
        return False
    return OBJ_SANMGMT.link_trigger(action="DOWN", addr=port_addr)


def _port_oscillate(port_addr):
    """
    Oscilate switch port
    """
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    if not port_addr:
        print("FAIL: port_oscillate() - requires port_addr as parameter")
        return False

    connected_sw = OBJ_SANMGMT.get_sw_self(port_addr)
    if not connected_sw:
        print("FAIL: %s is not managed by libsan" % port_addr)
        return False
    return OBJ_SANMGMT.link_oscillate(addr=port_addr)


def _phy_port_disconnect(port_addr):
    """
    Disable phy switch port
    """
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    if not port_addr:
        print("FAIL: phy_port_disconnect() - requires port_addr as parameter")
        return False

    connected_sw = OBJ_SANMGMT.get_physw_self(port_addr)
    if not connected_sw:
        print("FAIL: %s is not managed by libsan" % port_addr)
        return False
    return OBJ_SANMGMT.phy_link_trigger(action="DOWN", addr=port_addr)


def _port_connect(port_addr):
    """
    Enable switch port
    """
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    if not port_addr:
        print("FAIL: port_connect() - requires port_addr as parameter")
        return False

    connected_sw = OBJ_SANMGMT.get_sw_self(port_addr)
    if not connected_sw:
        print("FAIL: %s is not managed by libsan" % port_addr)
        return False
    return OBJ_SANMGMT.link_trigger(action="UP", addr=port_addr)


def _link_torture(port_addr, runtime, interval):
    """
    Bring switch port down and up for specific time
    """
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    if not port_addr or not runtime:
        print("FAIL: link_torture() - requires port_addr, runtime as parameteres")
        return False

    if interval is None:
        interval = 30

    interval = time_2_sec(interval)
    if interval is None:
        print("FAIL: link_torture() - Could not convert interval to seconds")
        return False

    time_in_sec = time_2_sec(runtime)
    if not time_in_sec:
        return True

    current_time = get_time(in_seconds=True)
    if not current_time:
        print("FAIL: link_torture() - Could not get current time")
        return False

    end_time = current_time + time_in_sec

    error = False
    while current_time < end_time:
        if not _port_disconnect(port_addr):
            error = True
        print("INFO: sleeping for %d seconds" % interval)
        libsan.host.linux.sleep(interval)
        if not _port_connect(port_addr):
            error = True
        if error:
            break
        print("INFO: sleeping for %d seconds" % interval)
        libsan.host.linux.sleep(interval)
        current_time = get_time(in_seconds=True)

    if error:
        # Try to bring port up
        print("Trying to bring %s back up" % port_addr)
        _port_connect(port_addr)
        return False

    return True


def _phy_port_connect(port_addr):
    """
    Enable phy switch port
    """
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    if not port_addr:
        print("FAIL: phy_port_connect() - requires port_addr as parameter")
        return False

    connected_sw = OBJ_SANMGMT.get_physw_self(port_addr)
    if not connected_sw:
        print("FAIL: %s is not managed by libsan" % port_addr)
        return False
    return OBJ_SANMGMT.phy_link_trigger(action="UP", addr=port_addr)


def _phy_port_oscillate(port_addr):
    """
    Oscilate phy switch port
    """
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    if not port_addr:
        print("FAIL: phy_port_oscillate() - requires port_addr as parameter")
        return False

    connected_sw = OBJ_SANMGMT.get_physw_self(port_addr)
    if not connected_sw:
        print("FAIL: %s is not managed by libsan" % port_addr)
        return False
    return OBJ_SANMGMT.phy_link_oscillate(addr=port_addr)


def _lun_create(lun_size, lun_name=None):
    """
    Create a LUN on array
    """
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    if not lun_size:
        print("FAIL: lun_create() - requires size as parameter")
        return None

    new_lun_name = OBJ_SANMGMT.lun_create(lun_size, lun_name=lun_name)
    if new_lun_name:
        print("INFO: created LUN %s" % new_lun_name)
        return new_lun_name
    print("FAIL: Could not create LUN")
    return None


def _lun_create_and_map(lun_size, lun_name=None):
    """
    Create a LUN to array and map it to server
    """
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: lun_create_and_map() - Could not create LibSAN object")
            sys.exit(1)

    if not lun_size:
        print("FAIL: lun_create_and_map() - requires size as parameter")
        return None

    new_lun_name = OBJ_SANMGMT.lun_create_and_map(lun_size, lun_name=lun_name, rescan=True)
    if new_lun_name:
        print("INFO: created and mapped LUN %s" % new_lun_name)
        return new_lun_name
    print("FAIL: Could not create LUN")
    return None


def _lun_remove(lun_name):
    """
    Remove LUN from array
    """
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    if not lun_name:
        print("FAIL: lun_remove() - requires lun_name as parameter")
        return False

    error = 0
    names = lun_name.split(",")
    for name in names:
        if not OBJ_SANMGMT.lun_remove(name):
            print("FAIL: Could not delete %s" % name)
            error += 1
    if error > 0:
        return False
    return True


def _lun_map(lun_name, t_addr=None, i_addr=None):
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    if not lun_name:
        print("FAIL: lun_map() - requires lun_name as parameter")
        return False

    return OBJ_SANMGMT.lun_map(lun_name, t_addr=t_addr, i_addr=i_addr, rescan=True)


def _lun_unmap(lun_name, t_addr=None, i_addr=None):
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    if not lun_name:
        print("FAIL: lun_unmap() - requires lun_name as parameter")
        return False

    return OBJ_SANMGMT.lun_unmap(lun_name, t_addr=t_addr, i_addr=i_addr)


def _lun_info(lun_name):
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    if not lun_name:
        print("FAIL: lun_info() - requires lun_name as parameter")
        return False

    info = OBJ_SANMGMT.lun_info(lun_name)
    if info:
        print(info)
        return True
    print("FAIL: Could not get info for %s" % lun_name)
    return False


def _lun_show():
    global OBJ_SANMGMT
    if not OBJ_SANMGMT:
        # Initialize SAN obj based on all information configured on /etc/san_top.cfg
        # based on HW information
        OBJ_SANMGMT = libsan.sanmgmt.create_sanmgmt_for_mpath()
        if not OBJ_SANMGMT:
            print("FAIL: Could not create LibSAN object")
            sys.exit(1)

    luns = OBJ_SANMGMT.lun_query()
    if not luns:
        return False
    for lun_name in luns:
        print("%s" % lun_name)
    return True


def _remove_device_wwid(wwid):
    return libsan.host.linux.remove_device_wwid(wwid)


def _rescan_host(hostid):
    return libsan.host.scsi.rescan_host(hostid)


def _dt_stress(of, log=None, thread=None, runtime=None):
    return libsan.host.dt.dt_stress(of, log=log, thread=thread, time=runtime)


def _dt_stress_background(of, log=None, thread=None, runtime=None):
    if libsan.host.dt.dt_stress_background(of, log=log, thread=thread, time=runtime):
        return True
    return False


def _fio_stress(of, threads=None, runtime=None, verify=None):
    ret, output = libsan.host.fio.fio_stress(
        of, threads=threads, runtime=runtime, verify=verify, return_output=True, time_based=None
    )
    if output:
        print(output)
    return ret


def _fio_stress_background(of, threads=None, runtime=None, verify=None):
    if libsan.host.fio.fio_stress_background(of, threads=threads, runtime=runtime, verify=verify):
        return True
    return False


arg_lun_name = {"name": "--name -n", "help": "Lun name", "dest": "lun_name"}
arg_lun_size = {
    "name": "--size -s",
    "help": "Lun Size. Eg. 2MiB, 2GiB,<F12> 2TiB",
    "dest": "lun_size",
    "metavar": "size",
    "required": True,
}
arg_init_addr = {
    "name": "--i_addr -i",
    "required": False,
    "dest": "i_addr",
    "metavar": "init_addr",
    "help": "Initiator address. IQN/WWPN",
}
arg_tgt_addr = {
    "name": "--t_addr -t",
    "required": False,
    "dest": "t_addr",
    "metavar": "target_addr",
    "help": "Target address. IQN/WWPN",
}
arg_port_addr = {
    "name": "--addr -a",
    "required": True,
    "dest": "port_addr",
    "metavar": "addr",
    "help": "WWPN/MAC of port",
}
arg_wwid = {"name": "--wwid -w", "required": True, "dest": "wwid", "metavar": "wwid", "help": "SCSI device WWID"}
arg_hostid = {"name": "--hostid -H", "required": False, "dest": "hostid", "metavar": "hostid", "help": "Host ID"}
arg_of = {
    "name": "--of -o",
    "required": True,
    "dest": "of",
    "metavar": "output",
    "help": "output, can be a device or file",
}
arg_runtime = {
    "name": "--time -t",
    "required": True,
    "dest": "runtime",
    "metavar": "time",
    "help": "For how long it should run",
}
arg_log = {"name": "--log -l", "required": False, "dest": "log", "metavar": "log", "help": "File to store log"}
arg_threads = {
    "name": "--thread -T",
    "required": False,
    "dest": "threads",
    "metavar": "threads",
    "help": "Number of threads",
}
arg_fio_verify = {
    "name": "--verify -V",
    "required": False,
    "dest": "verify",
    "metavar": "type",
    "choices": ["crc32c", "md5"],
}

cmds = (
    {
        "name": "show_san_conf",
        "help": "Show san_top config file",
        "func": _show_san_conf,
    },
    {
        "name": "show_host_config",
        "help": "Show information about host configuration",
        "func": _show_host_cfg,
    },
    {
        "name": "setup_soft_fcoe",
        "help": "Configure Soft FCoE",
        "func": libsan.host.fcoe.setup_soft_fcoe,
    },
    {
        "name": "create_basic_iscsi_target",
        "help": "Setup a basic iSCSI target",
        "func": libsan.host.lio.lio_setup_iscsi_target,
    },
    {
        "name": "lun_create",
        "help": "Create new LUN",
        "func": _lun_create,
        "args": [
            dict(arg_lun_name),
            dict(arg_lun_size),
        ],
    },
    {
        "name": "lun_create_and_map",
        "help": "Create new LUN and map it to target",
        "func": _lun_create_and_map,
        "args": [
            dict(arg_lun_name),
            dict(arg_lun_size),
        ],
    },
    {
        "name": "lun_remove",
        "help": "Remove LUN",
        "func": _lun_remove,
        "args": [
            dict(arg_lun_name, required=True),
        ],
    },
    {
        "name": "lun_map",
        "help": "Map a LUN to initiator/target",
        "func": _lun_map,
        "args": [
            dict(arg_lun_name, required=True),
            dict(arg_init_addr),
            dict(arg_tgt_addr),
        ],
    },
    {
        "name": "lun_unmap",
        "help": "Unmap a LUN from initiator/target",
        "func": _lun_unmap,
        "args": [
            dict(arg_lun_name, required=True),
            dict(arg_init_addr),
            dict(arg_tgt_addr),
        ],
    },
    {
        "name": "lun_info",
        "help": "Show information about specific LUN",
        "func": _lun_info,
        "args": [
            dict(arg_lun_name, required=True),
        ],
    },
    {
        "name": "lun_show",
        "help": "List all LUNs from the connected array",
        "func": _lun_show,
    },
    {
        "name": "check_ports_ready",
        "help": "Check if switch ports are ready",
        "func": _check_ports_ready,
    },
    {
        "name": "rcsn_enable",
        "help": "Enable RCSN on Switch",
        "func": _rcsn_enable,
        "args": [
            dict(arg_port_addr),
        ],
    },
    {
        "name": "rcsn_disable",
        "help": "Disable RCSN on Switch",
        "func": _rcsn_disable,
        "args": [
            dict(arg_port_addr),
        ],
    },
    {
        "name": "port_connect",
        "help": "Bring switch port online",
        "func": _port_connect,
        "args": [
            dict(arg_port_addr),
        ],
    },
    {
        "name": "port_disconnect",
        "help": "Bring switch port offline",
        "func": _port_disconnect,
        "args": [
            dict(arg_port_addr),
        ],
    },
    {
        "name": "port_oscillate",
        "help": "Oscillate switch port online/offline",
        "func": _port_oscillate,
        "args": [
            dict(arg_port_addr),
        ],
    },
    {
        "name": "link_torture",
        "help": "Bring switch port down and up for specific time",
        "func": _link_torture,
        "args": [
            dict(arg_port_addr),
        ],
    },
    {
        "name": "phy_port_connect",
        "help": "Bring phy switch port online",
        "func": _phy_port_connect,
        "args": [
            dict(arg_port_addr),
        ],
    },
    {
        "name": "phy_port_disconnect",
        "help": "Bring phy switch port offline",
        "func": _phy_port_disconnect,
        "args": [
            dict(arg_port_addr),
        ],
    },
    {
        "name": "phy_port_oscillate",
        "help": "Oscillate phy switch port online/offline",
        "func": _phy_port_oscillate,
        "args": [
            dict(arg_port_addr),
        ],
    },
    {
        "name": "remove_device_wwid",
        "help": "Remove an SCSI device based on it's WWID",
        "func": _remove_device_wwid,
        "args": [
            dict(arg_wwid),
        ],
    },
    {
        "name": "rescan_host",
        "help": "Rescan specific host ID",
        "func": _rescan_host,
        "args": [
            dict(arg_hostid),
        ],
    },
    {
        "name": "dt_stress",
        "help": "Run DT on specific path",
        "func": _dt_stress,
        "args": [
            dict(arg_of),
            dict(arg_runtime),
            dict(arg_log),
            dict(arg_threads),
        ],
    },
    {
        "name": "dt_stress_background",
        "help": "Run DT on background on specific path",
        "func": _dt_stress_background,
        "args": [
            dict(arg_of),
            dict(arg_runtime),
            dict(arg_log),
            dict(arg_threads),
        ],
    },
    {
        "name": "fio_stress",
        "help": "Run FIO on specific path",
        "func": _fio_stress,
        "args": [
            dict(arg_of),
            dict(arg_runtime),
            dict(arg_fio_verify),
            dict(arg_threads),
        ],
    },
    {
        "name": "fio_stress_background",
        "help": "Run FIO on background on specific path",
        "func": _fio_stress_background,
        "args": [
            dict(arg_of),
            dict(arg_runtime),
            dict(arg_fio_verify),
            dict(arg_threads),
        ],
    },
)


def main():
    parser = argparse.ArgumentParser(description="LibSAN tool")

    subparsers = parser.add_subparsers(help="Valid commands", dest="command")
    for cmd in cmds:
        _help = None
        if "help" in cmd:
            _help = cmd["help"]
        sub_parser = subparsers.add_parser(cmd["name"], help=_help)
        req_group = sub_parser.add_argument_group("required arguments")
        if "args" in cmd:
            for arg in cmd.get("args", []):
                name = arg.pop("name")
                required = False
                if "required" in arg:
                    required = arg.pop("required")
                if "dest" not in arg:
                    print("FAIL: dest needs to be set for arg: {} for command: {}".format(name, cmd["name"]))
                    sys.exit(1)
                name_list = name.split(" ")
                if required:
                    req_group.add_argument(*name_list, required=required, **arg)
                else:
                    sub_parser.add_argument(*name_list, required=required, **arg)

    args = parser.parse_args()

    for cmd in cmds:
        if cmd["name"] == args.command:
            if "func" not in cmd:
                print("FAIL: There is no function associated with %s" % cmd["name"])
                sys.exit(1)
            func = cmd["func"]
            func_args = vars(args)
            del func_args["command"]
            if func_args:
                if func(**func_args):
                    sys.exit(0)
            else:
                if func():
                    sys.exit(0)
            sys.exit(1)

    print("FAIL: Unsupported command: %s" % args.command)
    sys.exit(1)


main()
