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

.. currentmodule:: linuxnet.qos.qdisc

.. _queuing_statistics:

Queuing Statistics
------------------

All Python classes for queuing disciplines (and their queuing classes,
if classful) provide a :meth:`get_stats` method to access queuing statistics.
This method returns a :class:`QStats` object which contains the
statistics that are common across queuing disciplines/classes.
Queuing disciplines/classes (e.g. ``HTB``) that maintain additional
statistics subclass :class:`QStats` to provide access to those statistics.

.. _qstats:

QStats
~~~~~~

.. autoclass:: QStats
    :members:
    :member-order: bysource
