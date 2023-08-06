..
    Copyright (c) 2022, Panagiotis Tsirigotis
    
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

U32IPFilter
-----------

The :class:`U32IPFilter` uses the packet contents to classify a packet.
Matching is done using selector classes.
The following selector classes are available:

* :class:`IPSubnetSelector` : match based on ``IP`` subnet
* :class:`IPPortSelector` : match based on port
* :class:`IPProtocolSelector` : match based on protocol
* :class:`NumberSelector` : match based on packet contents at
  specified offset
* :class:`IPHeaderLength` : match based on ``IP`` header length
* :class:`IPDatagramLimit` : match based on datagram size
* :class:`TcpAck` : match based on presence of ``TCP`` ``ACK``

The class :class:`U32FilterHandle` describes the ``U32`` filter handle.

----------

.. autoclass:: U32IPFilter
    :inherited-members:
    :member-order: bysource

----------

.. autoclass:: U32FilterHandle
    :inherited-members:
    :member-order: bysource

----------

IPSubnetSelector
~~~~~~~~~~~~~~~~

.. autoclass:: IPSubnetSelector
    :inherited-members:
    :member-order: bysource


----------

IPPortSelector
~~~~~~~~~~~~~~

.. autoclass:: IPPortSelector
    :inherited-members:
    :member-order: bysource


----------

IPProtocolSelector
~~~~~~~~~~~~~~~~~~

.. autoclass:: IPProtocolSelector
    :inherited-members:
    :member-order: bysource


----------

NumberSelector
~~~~~~~~~~~~~~

.. autoclass:: NumberSelector
    :inherited-members:
    :member-order: bysource


----------

IPHeaderLength
~~~~~~~~~~~~~~

.. autoclass:: IPHeaderLength
    :inherited-members:
    :show-inheritance:
    :member-order: bysource


----------

IPDatagramLimit
~~~~~~~~~~~~~~~

.. autoclass:: IPDatagramLimit
    :inherited-members:
    :show-inheritance:
    :member-order: bysource


----------

TcpAck
~~~~~~

.. autoclass:: TcpAck
    :inherited-members:
    :show-inheritance:
    :member-order: bysource
