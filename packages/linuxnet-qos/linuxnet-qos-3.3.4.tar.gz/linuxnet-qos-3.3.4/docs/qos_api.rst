..
    Copyright (c) 2023, Panagiotis Tsirigotis
    
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

.. currentmodule:: linuxnet.qos

linuxnet.qos API
================

The **linuxnet.qos** API consists of the following:

- :class:`QDiscConfig` : objects of this class contain the queueing
  discipline configuration for a particular network interface
- :ref:`Classes <qdisc>` that provide access to queueing disciplines
  (e.g. :class:`HTBQDisc`); where those disciplines are classful,
  Python classes are available for the queueing discipline classes
  (e.g. :class:`HTBQClass`)
- Classes that provide access to queueing discipline
  :ref:`statistics <queuing_statistics>`; at a minimum, the statistics
  are those available
  via the :ref:`QStats <qstats>` class, but some queueing disciplines
  provide their own subclass with additional statistics
- :ref:`Classes <traffic_filter>` that provide access
  to traffic filters
- :ref:`Classes <traffic_action>` that provide access
  to traffic actions (e.g. policing)


.. toctree::
    :maxdepth: 2
    :hidden:

    config
    qdisc
    traffic_filters
    traffic_actions
    stats
    exceptions
    extensibility
