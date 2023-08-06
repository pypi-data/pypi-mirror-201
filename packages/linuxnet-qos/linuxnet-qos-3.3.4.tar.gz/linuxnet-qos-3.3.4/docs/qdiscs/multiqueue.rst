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

.. currentmodule:: linuxnet.qos

MQ
--

The following classes provide access to the ``mq``
(multi queue) queueing discipline:

* :class:`MultiQueueQDisc`
* :class:`MultiQueueQClass`

---------------

.. autoclass:: MultiQueueQDisc
    :inherited-members:
    :show-inheritance:
    :member-order: bysource
    :exclude-members: get_filters, create_filter, delete_filter

---------------

.. autoclass:: MultiQueueQClass
    :inherited-members:
    :show-inheritance:
    :member-order: bysource
    :exclude-members: get_filters, create_filter, delete_filter, get_child, get_child_count, get_child_iter, get_children
