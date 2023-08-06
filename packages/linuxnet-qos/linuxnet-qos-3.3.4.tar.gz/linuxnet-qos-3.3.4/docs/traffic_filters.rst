..
    Copyright (c) 2022, 2023, Panagiotis Tsirigotis
    
    This file is part of linuxnet-qos.
    
    linuxnet-qos is free software: you can redistribute it and/or
    modify it under the terms of version 3 of the GNU Affero General Public
    License as published by the Free Software Foundation.
    
    linuxnet-qos is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
    License for more details.
    
    You should have received a copy of the GNU Affero General
    Public License along with linuxnet-qos. If not, see
    <https://www.gnu.org/licenses/>.

.. _traffic_filter:

Traffic filters
===============

A traffic filter is a filter that directs traffic to a queuing class.
Matching is performed against the data in the ethernet frame (e.g.
IPv4 protocol number) or the metadata created by the Linux kernel
for the frame (e.g. firewall mark).

A traffic filter is attached to a queuing discipline or to a class
of a queuing discipline.

.. currentmodule:: linuxnet.qos

The **linuxnet.qos** package provides the following
traffic filter classes:

.. toctree::
    :maxdepth: 1
    :glob:

    filters/*
