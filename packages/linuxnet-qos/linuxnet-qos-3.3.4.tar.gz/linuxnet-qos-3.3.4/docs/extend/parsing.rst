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

.. currentmodule:: linuxnet.qos.extension

Parsers
-------

**linuxnet.qos** uses a number of parser classes to parse the output
of the **tc(8)** command:

* :class:`QDiscParser`
* :class:`QClassParser`
* :class:`TrafficFilterParser`

The following classes are also used in parsing:

* :class:`QDiscOutput`
* :class:`QClassOutput`
* :class:`FilterOutput`
* :class:`FilterOutputLine`

-----------------

.. _qdisc_parsing:

Queuing discipline parsing
~~~~~~~~~~~~~~~~~~~~~~~~~~

The :class:`QDiscParser` class is responsible for parsing the output of
``tc -s qdisc ls dev <interface>``.

The :meth:`QDiscParser.register_qdisc` method must be invoked
to register queueing discipline classes.

.. autoclass:: QDiscParser
   :members:
   :member-order: bysource

.. autoclass:: QDiscOutput
   :members:
   :inherited-members:
   :member-order: bysource

-----------------

.. _qclass_parsing:

Queuing class parsing
~~~~~~~~~~~~~~~~~~~~~

The :class:`QClassParser` class is responsible for parsing the output of
``tc -s class ls dev <interface>``.

The :meth:`QClassParser.register_qclass` method must be invoked
to register Python classes providing support for classes of
classful queueing disciplines.

.. autoclass:: QClassParser
   :members:
   :member-order: bysource

.. autoclass:: QClassOutput
   :members:
   :inherited-members:
   :member-order: bysource

-----------------

.. _filter_parsing:

Traffic filter parsing
~~~~~~~~~~~~~~~~~~~~~~

The :class:`TrafficFilterParser` class is responsible for parsing the output of
``tc filter ls dev <interface>``.

The :meth:`TrafficFilterParser.register_filter` method must be invoked
to register classes traffic filter classes.

.. autoclass:: TrafficFilterParser
   :members:
   :member-order: bysource

-------------

.. autoclass:: FilterOutput
   :members:
   :member-order: bysource

-------------

.. autoclass:: FilterOutputLine
   :members:
   :member-order: bysource
