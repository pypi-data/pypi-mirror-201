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

FQ_CODEL
--------

The following classes provides access to the ``fq_codel``
(Fair Queuing with Controlled Delay) queueing discipline
and its statistics:

* :class:`FQCoDelQDisc`
* :class:`FQCoDelQDiscStats`

---------------

.. autoclass:: FQCoDelQDisc
    :inherited-members:
    :show-inheritance:
    :member-order: bysource
    :exclude-members: get_child, get_child_count, get_child_iter, get_children, get_filters, create_filter, delete_filter


FQCoDelQDiscStats
~~~~~~~~~~~~~~~~~

.. autoclass:: FQCoDelQDiscStats
    :show-inheritance:
    :inherited-members:
    :members:
    :member-order: bysource
