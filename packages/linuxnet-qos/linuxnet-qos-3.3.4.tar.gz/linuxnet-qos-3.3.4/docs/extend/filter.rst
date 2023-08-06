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

Supporting a new traffic filter type
------------------------------------

The steps to add support for a new queuing discipline are:

#. Creation of a new Python class that inherits from :class:`TrafficFilter`;
   the convention is to name such a class ``xxxFilter``
   where  ``xxx`` is the name of the filter

   :meth:`xxxFilter.__init__` should expect as optional arguments:
   
   * the filter priority (an integer)
   * the :class:`Handle` of the destination queuing class
   * the filter-specific parameters

#. The ``xxxFilter`` class **must** implement the
   :meth:`filter_creation_args` method;
   this method should return the filter-specific **tc(8)** arguments for
   creating the filter

#. The ``xxxFilter`` class **must** implement the class method
   :meth:`parse` to create a ``xxxFilter`` instance from the
   :class:`FilterOutput` instance that is passed as an argument.

#. The ``xxxFilter`` class **must** be registered by invoking the
   :meth:`TrafficFilterParser.register_filter` method

#. The ``xxxFilter`` class **should** implement the
   :meth:`get_description` method

#. The ``xxxFilter`` class **should** implement the
   :meth:`get_match_name` method

#. The ``xxxFilter`` class **should** implement getter methods
   for the filter-specific parameters

#. The ``xxxFilter`` class **may** implement setter methods
   for the filter-specific parameters

--------------------

TrafficFilter
~~~~~~~~~~~~~

.. autoclass:: TrafficFilter
   :members:
   :member-order: bysource

