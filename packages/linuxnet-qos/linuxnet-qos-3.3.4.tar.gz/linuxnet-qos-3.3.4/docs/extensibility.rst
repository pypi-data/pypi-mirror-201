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

.. module:: linuxnet.qos.extension


Extensibility
=============

**linuxnet.qos** supports only a subset of the queuing disciplines and
traffic filters that are available in the Linux kernel.

Additional queuing disciplines can be supported by extending the
:class:`QDisc` and :class:`QClass` classes.

Additional traffic filters can be supported by extending the
:class:`TrafficFilter` class.

.. toctree::
    :maxdepth: 3

    extend/qdisc
    extend/filter
    extend/parsing
    extend/util
