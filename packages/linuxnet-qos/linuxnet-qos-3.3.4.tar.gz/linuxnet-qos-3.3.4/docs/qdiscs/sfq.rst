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

SFQ
---

The following classes provides access to the ``sfq``
(stochastic fairness queuing) queueing discipline
and its statistics:

* :class:`SFQQDisc`
* :class:`SFQQDiscStats`

---------------

.. autoclass:: SFQQDisc
    :inherited-members:
    :show-inheritance:
    :member-order: bysource
    :exclude-members: get_child, get_child_count, get_child_iter, get_children, get_filters, create_filter, delete_filter

---------------

.. autoclass:: SFQQDiscStats
    :show-inheritance:
    :members:
    :inherited-members:
    :exclude-members: init_from_output
    :member-order: bysource
