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

HTB
---

The following classes provide access to the ``htb``
(Hierarchy Token Bucket) queueing discipline and
its statistics:

* :class:`HTBQDisc`
* :class:`HTBQClass`
* :class:`HTBQClassStats`

---------------

.. autoclass:: HTBQDisc
    :inherited-members:
    :member-order: bysource

---------------

.. autoclass:: HTBQClass
    :inherited-members:
    :member-order: bysource

---------------

.. autoclass:: HTBQClassStats
    :show-inheritance:
    :members:
    :inherited-members:
    :member-order: bysource
