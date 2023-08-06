# Copyright (c) 2022, 2023, Panagiotis Tsirigotis

# This file is part of linuxnet-qos.
#
# linuxnet-qos is free software: you can redistribute it and/or
# modify it under the terms of version 3 of the GNU Affero General Public
# License as published by the Free Software Foundation.
#
# linuxnet-qos is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General
# Public License along with linuxnet-qos. If not, see
# <https://www.gnu.org/licenses/>.

"""Unit-test code for linuxnet.qos
"""

import logging
import os
import subprocess
import unittest
import sys

from collections import namedtuple
from ipaddress import IPv4Network

curdir = os.getcwd()
if os.path.basename(curdir) == 'tests':
    sys.path.insert(0, '..')
    TESTDIR = '.'
else:
    sys.path.insert(0, '.')
    TESTDIR = 'tests'

from linuxnet.qos import (
                        Handle,
                        QDiscConfig,
                        PFifoFastQDisc,
                        PrioQDisc, PrioQClass,
                        HTBQDisc, HTBQClass,
                        MultiQueueQDisc, MultiQueueQClass,
                        FQCoDelQDisc,
                        SFQQDisc,
                        NetemQDisc,
                        U32IPFilter,
                            IPSubnetSelector,
                        FwmarkIPFilter,
                        PoliceAction,
                        MirredAction,
                        ActionDecision,
                        )

root_logger = logging.getLogger()
root_logger.addHandler(logging.FileHandler('test.log', 'w'))
root_logger.setLevel(logging.INFO)


ExecutedCommand = namedtuple('ExecutedCommand', ['cmd', 'args', 'kwargs'])


class SimulatedTcRun:     # pylint: disable=too-few-public-methods
    """Simulate a run of the tc command
    """
    def __init__(self, exitcode, *,
                        qdisc_output=None,
                        qclass_output=None,
                        filter_output_map=None):
        self.__qdisc_output = qdisc_output
        self.__qclass_output = qclass_output
        # Key: parent handle
        # Value: output
        self.__filter_output_map = filter_output_map or {}
        self.__exitcode = exitcode
        # A run is a list of ExecutedCommand instances
        self.__run = []

    def set_filter_output(self, qdisc_handle_str, output):
        if output is None:
            self.__filter_output_map.pop(qdisc_handle_str, None)
        else:
            self.__filter_output_map[qdisc_handle_str] = output

    def get_run(self):
        return self.__run

    def clear_run(self):
        self.__run.clear()

    def __call__(self, *args, **kwargs):
        if not isinstance(args[0], list):
            raise Exception("1st arg is not a list")
        cmd = args[0]
        if cmd[0] != 'tc':
            raise Exception(f"invoking {cmd[0]} instead of 'tc'")
        if cmd[1] == '-s':
            objtype = cmd[2]
        else:
            objtype = cmd[1]
        if objtype == 'qdisc':
            output = self.__qdisc_output
        elif objtype == 'class':
            output = self.__qclass_output
        elif objtype == 'filter':
            parent_handle = cmd[cmd.index('parent') + 1]
            output = self.__filter_output_map.get(parent_handle, "")
        else:
            raise Exception(f"unexpected 'tc' argument {objtype}")
        self.__run.append(ExecutedCommand(cmd, args, kwargs))
        proc = subprocess.CompletedProcess(args, self.__exitcode)
        proc.stdout = output or ""
        return proc


class TestHTBQDisc(unittest.TestCase):
    """Test the HTB qdisc
    """

    def test_parsing_htb_qdisc(self):
        """Parse output for the htb qdisc
        """
        qdisc_output = """\
qdisc htb 1: root refcnt 2 r2q 10 default 0 direct_packets_stat 0
 Sent 8000 bytes 500 pkt (dropped 8, overlimits 2 requeues 1) 
 rate 400bit 30pps backlog 100b 3p requeues 1 
"""
        qclass_output = """\
class htb 1:1 root prio 0 rate 100000Kbit ceil 100000Kbit burst 1600b cburst 1600b 
 Sent 8000 bytes 500 pkt (dropped 8, overlimits 2 requeues 1) 
 rate 400bit 30pps backlog 100b 3p requeues 1 
 lended: 100 borrowed: 20 giants: 3
 tokens: 2000 ctokens: 2000
"""
        runner = SimulatedTcRun(0, qdisc_output=qdisc_output,
                                        qclass_output=qclass_output)
        config = QDiscConfig('eth0', runner=runner)
        root_qdisc = config.get_root_qdisc()
        self.assertTrue(isinstance(root_qdisc, HTBQDisc))
        self.assertEqual(root_qdisc.get_r2q(), 10)
        self.assertEqual(root_qdisc.get_handle(), Handle(1, 0))
        #
        # Verify qdisc stats
        #
        stats = root_qdisc.get_stats()
        self.assertEqual(stats.bitrate, 400)
        self.assertEqual(stats.packetrate, 30)
        self.assertEqual(stats.bytes_sent, 8000)
        self.assertEqual(stats.packets_sent, 500)
        self.assertEqual(stats.requeued_packets, 1)
        self.assertEqual(stats.get_byte_backlog(), 100)
        #
        # Verify child class
        #
        self.assertEqual(root_qdisc.get_child_count(), 1)
        htb_qclass = root_qdisc.get_children()[0]
        self.assertTrue(isinstance(htb_qclass, HTBQClass))
        self.assertEqual(htb_qclass.get_handle(), Handle(1, 1))
        #
        # Verify class stats
        #
        stats = htb_qclass.get_stats()
        self.assertEqual(stats.bitrate, 400)
        self.assertEqual(stats.packetrate, 30)
        self.assertEqual(stats.bytes_sent, 8000)
        self.assertEqual(stats.packets_sent, 500)
        self.assertEqual(stats.requeued_packets, 1)
        self.assertEqual(stats.get_byte_backlog(), 100)
        self.assertEqual(stats.packets_lent, 100)
        self.assertEqual(stats.packets_borrowed, 20)
        self.assertEqual(stats.giant_packets, 3)
        self.assertEqual(stats.tokens, 2000)
        self.assertEqual(stats.ctokens, 2000)


class TestPFifoFastQDisc(unittest.TestCase):
    """Test the pfifo_fast qdisc
    """

    def test_parsing_pfifo_fast_qdisc(self):
        """Parse output for the pfifo_fast qdisc
        """
        qdisc_output = """\
qdisc pfifo_fast 0: root refcnt 2 bands 3 priomap  1 2 2 2 1 2 0 0 1 1 1 1 1 1 1 1
"""
        runner = SimulatedTcRun(0, qdisc_output=qdisc_output, qclass_output="")
        config = QDiscConfig('eth0', runner=runner)
        root_qdisc = config.get_root_qdisc()
        self.assertTrue(isinstance(root_qdisc, PFifoFastQDisc))


class TestMultiQueueQDisc(unittest.TestCase):
    """Test the multiqueue qdisc
    """

    def test_parsing_multiqueue_qdisc(self):
        """Parse output for the multiqueue qdisc
        """
        qdisc_output = """\
qdisc mq 0: root
 Sent 1785439436 bytes 12052219 pkt (dropped 0, overlimits 0 requeues 1393)
 backlog 0b 0p requeues 1393
"""
        qclass_output = """\
class mq :1 root
 Sent 9211399347 bytes 74550127 pkt (dropped 0, overlimits 0 requeues 1341)
 backlog 0b 0p requeues 1341
class mq :2 root
 Sent 1705270911 bytes 10946627 pkt (dropped 0, overlimits 0 requeues 361)
 backlog 0b 0p requeues 361
class mq :3 root
 Sent 4461798109 bytes 16328516 pkt (dropped 0, overlimits 0 requeues 11845)
 backlog 0b 0p requeues 11845
class mq :4 root
 Sent 2476427218 bytes 18700166 pkt (dropped 0, overlimits 0 requeues 392)
 backlog 0b 0p requeues 392
"""
        runner = SimulatedTcRun(0, qdisc_output=qdisc_output,
                                        qclass_output=qclass_output)
        config = QDiscConfig('eth0', runner=runner)
        root_qdisc = config.get_root_qdisc()
        self.assertTrue(isinstance(root_qdisc, MultiQueueQDisc))
        self.assertTrue(root_qdisc.is_root())
        self.assertTrue(root_qdisc.is_default())
        self.assertEqual(root_qdisc.get_handle(), Handle(0,0))
        #
        # Verify qdisc stats
        #
        stats = root_qdisc.get_stats()
        self.assertEqual(stats.bytes_sent, 1785439436)
        self.assertEqual(stats.packets_sent, 12052219)
        self.assertEqual(stats.requeued_packets, 1393)
        self.assertEqual(stats.get_byte_backlog(), 0)
        #
        # Verify child classes
        #
        self.assertEqual(root_qdisc.get_child_count(), 4)
        for minor, qclass in enumerate(root_qdisc.get_children(), 1):
            self.assertTrue(isinstance(qclass, MultiQueueQClass))
            self.assertEqual(qclass.get_handle(), Handle(0, minor))
            #
            # Verify class stats
            #
            stats = qclass.get_stats()
            if minor == 1:
                self.assertEqual(stats.bytes_sent, 9211399347)
            elif minor == 2:
                self.assertEqual(stats.packets_sent, 10946627)
            elif minor == 3:
                self.assertEqual(stats.requeued_packets, 11845)
            elif minor == 4:
                self.assertEqual(stats.dropped_packets, 0)


class TestPrioQDisc(unittest.TestCase):
    """Test the Prio qdisc
    """

    def test_parsing_prio_qdisc(self):
        """Parse output for the prio qdisc
        """
        qdisc_output = """\
qdisc prio 1: root refcnt 2 bands 2 priomap  1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
 Sent 0 bytes 0 pkt (dropped 0, overlimits 0 requeues 0) 
 rate 0bit 0pps backlog 0b 0p requeues 0 
"""
        qclass_output = """\
class prio 1:1 parent 1: 
 Sent 0 bytes 0 pkt (dropped 0, overlimits 0 requeues 0) 
 backlog 0b 0p requeues 0 
class prio 1:2 parent 1: 
 Sent 0 bytes 0 pkt (dropped 0, overlimits 0 requeues 0) 
 backlog 0b 0p requeues 0 
"""
        runner = SimulatedTcRun(0, qdisc_output=qdisc_output,
                                        qclass_output=qclass_output)
        config = QDiscConfig('eth0', runner=runner)
        root_qdisc = config.get_root_qdisc()
        self.assertTrue(isinstance(root_qdisc, PrioQDisc))
        self.assertTrue(root_qdisc.is_root())
        self.assertEqual(root_qdisc.get_handle(), Handle(1, 0))
        self.assertEqual(root_qdisc.get_bands(), 2)
        for i, band in enumerate(root_qdisc.get_priomap(), 1):
            self.assertEqual(i & 0x1, band)
        #
        # Verify qdisc stats
        #
        stats = root_qdisc.get_stats()
        self.assertEqual(stats.bytes_sent, 0)
        self.assertEqual(stats.packets_sent, 0)
        self.assertEqual(stats.requeued_packets, 0)
        self.assertEqual(stats.get_byte_backlog(), 0)
        #
        # Verify child classes
        #
        self.assertEqual(root_qdisc.get_child_count(), 2)
        for minor, qclass in enumerate(root_qdisc.get_children(), 1):
            self.assertTrue(isinstance(qclass, PrioQClass))
            self.assertEqual(qclass.get_handle(), Handle(1, minor))
            #
            # Verify class stats
            #
            stats = qclass.get_stats()
            if minor == 1:
                self.assertEqual(stats.bytes_sent, 0)
            elif minor == 2:
                self.assertEqual(stats.packets_sent, 0)


class TestFQCoDelQDisc(unittest.TestCase):
    """Test the fq_codel qdisc
    """

    def test_parsing_fq_codel_qdisc(self):
        """Parse output for the fq_codel qdisc
        """
        qdisc_output = """\
qdisc mq 0: root
 Sent 1785439436 bytes 12052219 pkt (dropped 0, overlimits 0 requeues 1393)
 backlog 0b 0p requeues 1393
qdisc fq_codel 0: parent :1 limit 10240p flows 1024 quantum 1514 target 5ms interval 100ms memory_limit 32Mb ecn drop_batch 64
 Sent 9214679423 bytes 74565506 pkt (dropped 0, overlimits 0 requeues 1346)
 backlog 0b 0p requeues 1346
  maxpacket 48016 drop_overlimit 0 new_flow_count 5060 ecn_mark 0
  new_flows_len 0 old_flows_len 0
"""
        qclass_output = """\
class mq :1 root
 Sent 9211399347 bytes 74550127 pkt (dropped 0, overlimits 0 requeues 1341)
 backlog 0b 0p requeues 1341
"""
        runner = SimulatedTcRun(0, qdisc_output=qdisc_output,
                                        qclass_output=qclass_output)
        codel_major = QDiscConfig._qdisc_remap_major
        config = QDiscConfig('eth0', runner=runner)
        root_qdisc = config.get_root_qdisc()
        self.assertTrue(isinstance(root_qdisc, MultiQueueQDisc))
        self.assertTrue(root_qdisc.is_root())
        #
        # Verify child class
        #
        qclass = root_qdisc.get_child(Handle(0, 1))
        self.assertTrue(isinstance(qclass, MultiQueueQClass))
        self.assertTrue(qclass.is_leaf())
        qdisc = qclass.get_qdisc()
        self.assertTrue(isinstance(qdisc, FQCoDelQDisc))
        self.assertEqual(qdisc.get_parent_handle(), qclass.get_handle())
        self.assertEqual(qdisc.get_handle(), Handle(codel_major, 0))
        self.assertEqual(qdisc.get_packet_limit(), 10240)
        self.assertEqual(qdisc.get_flows(), 1024)
        self.assertEqual(qdisc.get_quantum(), 1514)
        self.assertEqual(qdisc.get_queue_delay_target(), 5)
        self.assertEqual(qdisc.get_queue_delay_interval(), 100)
        self.assertEqual(qdisc.get_memory_limit(), 32*1000*1000)
        self.assertTrue(qdisc.get_ecn())
        #
        # Verify qdisc stats
        #
        stats = qdisc.get_stats()
        self.assertEqual(stats.bytes_sent, 9214679423)
        self.assertEqual(stats.maxpacket, 48016)
        self.assertEqual(stats.new_flow_count, 5060)
        self.assertEqual(stats.old_flows_len, 0)


class TestSFQQDisc(unittest.TestCase):
    """Test the SFQ qdisc
    """

    def test_parsing_sfq_qdisc(self):
        """Parse output for the sfq qdisc
        """
        qdisc_output = """\
qdisc sfq 2: root refcnt 2 limit 127p quantum 1500b perturb 10sec 
 Sent 0 bytes 0 pkt (dropped 0, overlimits 0 requeues 0) 
 rate 0bit 0pps backlog 0b 0p requeues 0 
"""
        runner = SimulatedTcRun(0, qdisc_output=qdisc_output,
                                        qclass_output="")
        config = QDiscConfig('eth0', runner=runner)
        root_qdisc = config.get_root_qdisc()
        self.assertTrue(isinstance(root_qdisc, SFQQDisc))
        self.assertTrue(root_qdisc.is_root())
        self.assertEqual(root_qdisc.get_handle(), Handle(2, 0))
        self.assertEqual(root_qdisc.get_quantum(), 1500)
        self.assertEqual(root_qdisc.get_perturb(), 10)
        #
        # Verify qdisc stats
        #
        stats = root_qdisc.get_stats()
        self.assertEqual(stats.bytes_sent, 0)


class TestNetemQDisc(unittest.TestCase):
    """Test the netem qdisc
    """

    def test_parsing_netem_qdisc(self):
        """Parse output for the netem qdisc
        """
        qdisc_output = """\
qdisc netem 3: root refcnt 2 limit 100 delay 10.0ms  1.0ms 10% loss 3% 20% duplicate 2% 33% reorder 12% 40% corrupt 5% gap 120
"""
        runner = SimulatedTcRun(0, qdisc_output=qdisc_output,
                                        qclass_output="")
        config = QDiscConfig('eth0', runner=runner)
        qdisc = config.get_root_qdisc()
        self.assertTrue(isinstance(qdisc, NetemQDisc))
        self.assertTrue(qdisc.is_root())
        self.assertEqual(qdisc.get_handle(), Handle(3, 0))
        self.assertEqual(qdisc.get_limit(), 100)
        self.assertEqual(qdisc.get_delay(), 10.0)
        self.assertEqual(qdisc.get_loss(), 3)
        self.assertEqual(qdisc.get_duplicate(), 2)
        self.assertEqual(qdisc.get_reorder(), 12)
        self.assertEqual(qdisc.get_corrupt(), 5)
        self.assertEqual(qdisc.get_gap(), 120)
        self.assertEqual(qdisc.get_delay_all(), (10.0, 1.0, 10))
        self.assertEqual(qdisc.get_reorder_all(), (12, 40))


class TestIngressQDisc(unittest.TestCase):
    """Test the ingress qdisc
    """

    def test_parsing_ingress_qdisc(self):
        """Parse output for the ingress qdisc
        """
        qdisc_output = """\
qdisc netem 1: root refcnt 2 limit 1000 delay 30.0ms
 Sent 0 bytes 0 pkt (dropped 0, overlimits 0 requeues 0)
 rate 0bit 0pps backlog 0b 0p requeues 0
qdisc ingress ffff: parent ffff:fff1 ----------------
 Sent 0 bytes 0 pkt (dropped 0, overlimits 0 requeues 0)
 rate 0bit 0pps backlog 0b 0p requeues 0
"""
        runner = SimulatedTcRun(0, qdisc_output=qdisc_output,
                                        qclass_output="")
        config = QDiscConfig('eth0', runner=runner)
        qdisc = config.get_ingress_qdisc()
        self.assertTrue(qdisc is not None)
        self.assertEqual(qdisc.get_handle(), Handle(0xffff, 0))
        runner.clear_run()
        config.delete_ingress_qdisc()
        commands = runner.get_run()
        expected_cmd = ['tc', 'qdisc', 'del', 'dev', 'eth0', 'ingress']
        self.assertEqual(commands[0].cmd, expected_cmd)
        self.assertTrue(config.get_ingress_qdisc() is None)


class TestFilterParsing(unittest.TestCase):
    """Test parsing of tc output for qdiscs
    """

    def test_parsing_u32filter(self):
        """Parse output for the u32 filter
        """
        qdisc_output = """\
qdisc htb 1: root refcnt 2 r2q 10 default 0 direct_packets_stat 0
"""
        # Output of 'tc filter ls parent <handle>' where handle is the key
        # of the dictionary.
        filter_output_map = {
            '1:0' : """\
filter protocol [768] pref 1 u32 
filter protocol [768] pref 1 u32 fh 801: ht divisor 1 
filter protocol [768] pref 1 u32 fh 801::800 order 2048 key ht 801 bkt 0 link 1: 
  match c0a80000/ffff0000 at 12
    hash mask 0000ff00 at 12 
filter protocol ip pref 99 u32 
filter protocol ip pref 99 u32 fh 1: ht divisor 256 
filter protocol ip pref 99 u32 fh 1:8:800 order 2048 key ht 1 bkt 8 flowid 1:1 
  match c0a80800/ffffff00 at 12
filter protocol [768] pref 99 u32 fh 800: ht divisor 1 
filter protocol ip pref 513 u32 
filter protocol ip pref 513 u32 fh 80e: ht divisor 1 
filter protocol ip pref 513 u32 fh 80e::800 order 2048 key ht 80e bkt 0 flowid 1:202 
  match 000003e1/0000ffff at 20
filter protocol ip pref 514 u32 
filter protocol ip pref 514 u32 fh 80f: ht divisor 1 
filter protocol ip pref 514 u32 fh 80f::800 order 2048 key ht 80f bkt 0 flowid 1:202 
  match 0000024b/0000ffff at 20
"""
                }
        runner = SimulatedTcRun(0, qdisc_output=qdisc_output,
                                    qclass_output="",
                                    filter_output_map=filter_output_map)
        config = QDiscConfig('eth0', runner=runner, allow_parsing_errors=True)
        self.assertEqual(config.get_error_count(), 0)
        root_qdisc = config.get_root_qdisc()
        # The following call will trigger reading of filters
        filter_list = root_qdisc.get_filters()
        #
        # Two errors caused by
        #       ('[768]', 1, 'u32')
        #       ('[768]', 99, 'u32')
        #
        self.assertEqual(config.get_error_count(), 2)
        self.assertEqual(len(filter_list), 3)
        #
        # The first filter is the one with priority 99
        #
        traffic_filter = filter_list[0]
        self.assertTrue(isinstance(traffic_filter, U32IPFilter))
        self.assertEqual(traffic_filter.get_prio(), 99)
        selectors = traffic_filter.get_selectors()
        self.assertEqual(len(selectors), 1)
        selector = selectors[0]
        self.assertTrue(isinstance(selector, IPSubnetSelector))
        self.assertEqual(selector.get_direction(), 'src')
        self.assertEqual(selector.get_prefix(), 24)
        #
        # The second filter is the one with priority 513
        #
        traffic_filter = filter_list[1]
        self.assertTrue(isinstance(traffic_filter, U32IPFilter))
        self.assertEqual(traffic_filter.get_prio(), 513)
        #
        # The second filter is the one with priority 514
        #
        traffic_filter = filter_list[2]
        self.assertTrue(isinstance(traffic_filter, U32IPFilter))
        self.assertEqual(traffic_filter.get_prio(), 514)

    def test_parsing_u32filter_with_policing(self):
        """Parse output for a u32 filter with policing
        """
        qdisc_output = """\
qdisc netem 1: root refcnt 2 limit 1000 delay 30.0ms
qdisc ingress ffff: parent ffff:fff1 ----------------
"""
        # Output of 'tc filter ls parent <handle>' where handle is the key
        # of the dictionary.
        filter_output_map = {
            'ffff:0' : """\
filter protocol ip pref 60 u32 chain 0
filter protocol ip pref 60 u32 chain 0 fh 801: ht divisor 1
filter protocol ip pref 60 u32 chain 0 fh 801::800 order 2048 key ht 801 bkt 0 terminal flowid not_in_hw
  match 00000000/00000000 at 16
 police 0x2 rate 256Kbit burst 10Kb mtu 2Kb action drop overhead 0b
        ref 1 bind 1
"""
                }
        runner = SimulatedTcRun(0, qdisc_output=qdisc_output,
                                    qclass_output="",
                                    filter_output_map=filter_output_map)
        config = QDiscConfig('eth0', runner=runner)
        ingress_qdisc = config.get_ingress_qdisc()
        filter_list = ingress_qdisc.get_filters()
        self.assertEqual(len(filter_list), 1)
        traffic_filter = filter_list[0]
        self.assertTrue(isinstance(traffic_filter, U32IPFilter))
        self.assertEqual(traffic_filter.get_prio(), 60)
        actions = traffic_filter.get_actions()
        self.assertEqual(len(actions), 1)
        #
        # The action is a police action
        #
        police_action = actions[0]
        self.assertEqual(police_action.get_kind(), 'police')
        self.assertEqual(police_action.get_action_index(), 2)
        self.assertEqual(police_action.get_burst(), 10*1000)
        self.assertEqual(police_action.get_mtu(), 2000)

    def test_parsing_u32filter_with_actions(self):
        """Parse output for a u32 filter with actions
        """
        qdisc_output = """\
qdisc netem 1: root refcnt 2 limit 1000 delay 30.0ms
qdisc ingress ffff: parent ffff:fff1 ----------------
"""
        # Output of 'tc filter ls parent <handle>' where handle is the key
        # of the dictionary.
        filter_output_map = {
            'ffff:0' : """\
filter protocol ip pref 70 u32 chain 0
filter protocol ip pref 70 u32 chain 0 fh 805: ht divisor 1
filter protocol ip pref 70 u32 chain 0 fh 805::800 order 2048 key ht 805 bkt 0 terminal flowid not_in_hw
  match 00000000/00000000 at 12
        action order 1:  police 0x1 rate 2048Kbit burst 10Kb mtu 2Kb action drop overhead 0b
        ref 1 bind 1

        action order 2: mirred (Egress Redirect to device lo) stolen
        index 2 ref 1 bind 1
"""
                }
        runner = SimulatedTcRun(0, qdisc_output=qdisc_output,
                                    qclass_output="",
                                    filter_output_map=filter_output_map)
        config = QDiscConfig('eth0', runner=runner)
        qdisc_map = config.get_qdisc_map()
        self.assertEqual(len(qdisc_map), 2)
        self.assertTrue(Handle(0xffff, 0) in qdisc_map)
        ingress_qdisc = config.get_ingress_qdisc()
        filter_list = ingress_qdisc.get_filters()
        self.assertEqual(len(filter_list), 1)
        traffic_filter = filter_list[0]
        self.assertTrue(isinstance(traffic_filter, U32IPFilter))
        self.assertEqual(traffic_filter.get_prio(), 70)
        actions = traffic_filter.get_actions()
        self.assertEqual(len(actions), 2)
        #
        # The 1st action is a police action
        #
        police_action = actions[0]
        self.assertEqual(police_action.get_kind(), 'police')
        self.assertEqual(police_action.get_action_index(), 1)
        #
        # The 2nd action is a mirred action
        #
        mirred_action = actions[1]
        self.assertEqual(mirred_action.get_kind(), 'mirred')
        self.assertEqual(mirred_action.get_action_index(), 2)

    def test_parsing_fwfilter(self):
        """Parse output for the fw filter
        """
        qdisc_output = """\
qdisc htb 1: root refcnt 2 r2q 10 default 0 direct_packets_stat 0
"""
        # Output of 'tc filter ls parent <handle>' where handle is the key
        # of the dictionary.
        filter_output_map = {
            '1:0' : """\
filter protocol ip pref 512 fw
filter protocol ip pref 512 fw handle 0x100 classid 1:200
filter protocol ip pref 10000 u32
filter protocol ip pref 10000 u32 fh 806: ht divisor 1
filter protocol ip pref 10000 u32 fh 806::800 order 2048 key ht 806 bkt 0 flowid 1:100
  match 00000000/00000000 at 16
"""
                }
        runner = SimulatedTcRun(0, qdisc_output=qdisc_output,
                                    qclass_output="",
                                    filter_output_map=filter_output_map)
        config = QDiscConfig('eth0', runner=runner)
        root_qdisc = config.get_root_qdisc()
        filter_list = root_qdisc.get_filters()
        self.assertEqual(len(filter_list), 2)
        traffic_filter = filter_list[0]
        self.assertTrue(isinstance(traffic_filter, FwmarkIPFilter))
        self.assertEqual(traffic_filter.get_fwmark(), 0x100)
        self.assertEqual(traffic_filter.get_dest_handle(), Handle(1, 0x200))

    def test_parsing_fwfilter_with_policing(self):
        """Parse output for the fw filter
        """
        qdisc_output = """\
qdisc htb 1: root refcnt 2 r2q 10 default 0 direct_packets_stat 0
qdisc ingress ffff: parent ffff:fff1 ----------------
"""
        # Output of 'tc filter ls parent <handle>' where handle is the key
        # of the dictionary.
        filter_output_map = {
            'ffff:0' : """\
filter protocol ip pref 20 fw chain 0
filter protocol ip pref 20 fw chain 0 handle 0x1 classid :1  police 0x4 rate 1Kbit burst 40b mtu 9Kb action drop overhead 0b
        ref 1 bind 1
"""
                }
        runner = SimulatedTcRun(0, qdisc_output=qdisc_output,
                                    qclass_output="",
                                    filter_output_map=filter_output_map)
        config = QDiscConfig('eth0', runner=runner)
        ingress_qdisc = config.get_ingress_qdisc()
        filter_list = ingress_qdisc.get_filters()
        self.assertEqual(len(filter_list), 1)
        traffic_filter = filter_list[0]
        self.assertTrue(isinstance(traffic_filter, FwmarkIPFilter))
        actions = traffic_filter.get_actions()
        self.assertEqual(len(actions), 1)
        police_action = actions[0]
        self.assertEqual(police_action.get_kind(), 'police')
        self.assertEqual(police_action.get_action_index(), 4)
        self.assertEqual(police_action.get_mtu(), 9000)
        self.assertEqual(police_action.get_decision(), ActionDecision.DROP)


class TestFilterCreation(unittest.TestCase):
    """Test creation of tc filters
    """

    def test_creation_u32filter(self):
        """Create a u32 filter
        """
        runner = SimulatedTcRun(0)
        expected_commands = []
        interface = 'eth1'
        config = QDiscConfig(interface, runner=runner,
                                        read_interface_config=False)
        qdisc = config.create_ingress_qdisc()
        expected_commands.append("tc qdisc add dev eth1 ingress")
        u32flt = U32IPFilter(prio=10, filter_name="test-filter",
                                dest_class_handle=Handle(0xa, 1))
        u32flt.add_selector(IPSubnetSelector('src', IPv4Network('0.0.0.0/0')))
        expected_commands.append(
                f"tc filter add dev {interface} parent {qdisc.get_handle()} "
                "protocol ip prio 10 u32 match ip src 0.0.0.0/0 flowid a:1"
                )
        qdisc.create_filter(u32flt)
        run = runner.get_run()
        for i, exec_cmd in enumerate(run):
            self.assertEqual(exec_cmd.cmd, expected_commands[i].split())

    def test_creation_fwfilter(self):
        """Create a fw filter
        """
        runner = SimulatedTcRun(0)
        expected_commands = []
        interface = 'eth1'
        config = QDiscConfig(interface, runner=runner,
                                        read_interface_config=False)
        qdisc = config.create_ingress_qdisc()
        expected_commands.append("tc qdisc add dev eth1 ingress")
        fwflt = FwmarkIPFilter(prio=3, fwmark=20,
                                dest_class_handle=Handle(0xa, 1))
        expected_commands.append(
                f"tc filter add dev {interface} parent {qdisc.get_handle()} "
                "protocol ip prio 3 handle 20 fw classid a:1"
                )
        qdisc.create_filter(fwflt)
        run = runner.get_run()
        for i, exec_cmd in enumerate(run):
            self.assertEqual(exec_cmd.cmd, expected_commands[i].split())


class TestActionCreation(unittest.TestCase):
    """Test creation of tc actions
    """

    def test_creation_police_action(self):
        """Create a police action
        """
        runner = SimulatedTcRun(0)
        expected_commands = []
        interface = 'eth1'
        config = QDiscConfig(interface, runner=runner,
                                        read_interface_config=False)
        qdisc = config.create_ingress_qdisc()
        expected_commands.append("tc qdisc add dev eth1 ingress")
        u32flt = U32IPFilter(prio=10, filter_name="test-filter",
                                dest_class_handle=Handle(0xa, 1))
        u32flt.add_selector(IPSubnetSelector('src', IPv4Network('0.0.0.0/0')))
        police_action = PoliceAction(rate=20*1000, burst=10*1000,
                                decision=ActionDecision.DROP)
        u32flt.add_action(police_action)
        expected_commands.append(
                f"tc filter add dev {interface} parent {qdisc.get_handle()} "
                "protocol ip prio 10 u32 match ip src 0.0.0.0/0 flowid a:1 "
                "action police rate 20000 burst 10000 drop"
                )
        qdisc.create_filter(u32flt)
        run = runner.get_run()
        for i, exec_cmd in enumerate(run):
            self.assertEqual(exec_cmd.cmd, expected_commands[i].split())

    def test_creation_mirred_action(self):
        """Create a mirred action
        """
        runner = SimulatedTcRun(0)
        expected_commands = []
        interface = 'eth1'
        config = QDiscConfig(interface, runner=runner,
                                        read_interface_config=False)
        qdisc = config.create_ingress_qdisc()
        expected_commands.append("tc qdisc add dev eth1 ingress")
        u32flt = U32IPFilter(prio=10, filter_name="test-filter",
                                dest_class_handle=Handle(0xa, 1))
        u32flt.add_selector(IPSubnetSelector('src', IPv4Network('0.0.0.0/0')))
        mirred_action = MirredAction(21,
                                mirred_action=MirredAction.MIRROR,
                                direction=MirredAction.INGRESS,
                                to_dev='lo')
        u32flt.add_action(mirred_action)
        expected_commands.append(
                f"tc filter add dev {interface} parent {qdisc.get_handle()} "
                "protocol ip prio 10 u32 match ip src 0.0.0.0/0 flowid a:1 "
                "action mirred index 21 ingress mirror dev lo"
                )
        qdisc.create_filter(u32flt)
        run = runner.get_run()
        for i, exec_cmd in enumerate(run):
            self.assertEqual(exec_cmd.cmd, expected_commands[i].split())

if __name__ == '__main__':
    unittest.main()
