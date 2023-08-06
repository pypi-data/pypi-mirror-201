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

.. currentmodule:: linuxnet.qos.qdiscs.ingress

INGRESS
-------

The :class:`IngressQDisc` class provides access to the ``ingress``
queueing discipline.

.. currentmodule:: linuxnet.qos

Instances of this class are not instantiated directly. Instead,
they are created via :meth:`QDiscConfig.create_ingress_qdisc`.

.. currentmodule:: linuxnet.qos.qdiscs.ingress

---------------

.. autoclass:: IngressQDisc
    :inherited-members:
    :show-inheritance:
    :member-order: bysource
    :exclude-members: get_child, get_child_count, get_child_iter, get_children
