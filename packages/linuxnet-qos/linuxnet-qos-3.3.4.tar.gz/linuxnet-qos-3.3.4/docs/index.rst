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

linuxnet.qos: a Python package for managing Linux QoS using tc
==============================================================

.. module:: linuxnet.qos

Release v\ |version|.

**linuxnet.qos** provides programmatic access to the
**tc(8)** command.
Using **linuxnet.qos** one can manipulate the Linux Traffic Control
functionality (queuing disciplines).

Accessing an interface's queuing discipline configuration::

    >>> from linuxnet.qos import QDiscConfig
    >>> config = QDiscConfig('eth2')
    >>> config.dump()
    PFifoFastQDisc(0:0) root bands 3 priomap 1 2 2 2 1 2 0 0 1 1 1 1 1 1 1 1

:class:`PFifoFastQDisc` is the Python class used to represent the
``pfifo_fast`` queuing discipline (see **tc-pfifo_fast(8)**).

Replacing the interface's root queuing discipline::

    >>> from linuxnet.qos import NetemQDisc, Handle
    >>> netem_qdisc = NetemQDisc(Handle(1,1), None, delay=30.0)
    >>> config.create_qdisc(netem_qdisc)
    >>> config.dump()
    NetemQDisc(1:1) root delay 30.0ms

Deleting the existing queuing discipline configuration::

    >>> config.delete_config()
    >>> config.read_interface_config()
    True
    >>> config.dump()
    PFifoFastQDisc(0:0) root bands 3 priomap 1 2 2 2 1 2 0 0 1 1 1 1 1 1 1 1


API Documentation
-----------------

.. toctree::
   :maxdepth: 3
   :includehidden:

   qos_api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
