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

Supporting a new queuing discipline
-----------------------------------

The following example illustrates how to add support for the ``pfifo``
queuing discipline::

    from linuxnet.qos.extension import (QDisc, unitstr2num,
                                        QDiscParser, QDiscOutput)

    class PFifoQDisc(QDisc):
        """The new Python class must be a child of QDisc
        """
        def __init__(self, handle, parent_handle, packet_limit=None):
            super().__init__(handle, parent_handle)
            self.__packet_limit = packet_limit

        def qdisc_creation_args(self):
            """This method is required; it should return the queuing
            discipline-specific tc(8) arguments for creating this
            queuing discipline
            """
            args = ['pfifo']
            if self.__packet_limit is not None:
                args.extend(['limit', str(self.__packet_limit)])
            return args

        def get_description(self):
            """This method is optional but recommended; it returns a
            description of the particular queuing discipline instantation
            """
            retval = super().get_description()
            if self.__packet_limit is not None:
                retval += f' limit {self.__packet_limit} packets'
            return retval

        def get_packet_limit(self):
            """This is a pfifo-specific method
            """
            return self.__packet_limit

        @classmethod
        def parse(cls, qdisc_output: QDiscOutput):
            """This method is required. It creates a PFifoQDisc instance
            from the output of tc(8).
            """
            field_iter = qdisc_output.get_field_iter()
            packet_limit = None
            for field in field_iter:
                if field == 'limit':
                    limitstr = next(field_iter)
                    # limit value should have 'p' suffix
                    packet_limit = unitstr2num(limitstr, 'p')
            return PFifoQDisc(qdisc_output.get_handle(),
                                    qdisc_output.get_parent_handle(),
                                    packet_limit)

    #
    # Register the new queueing discipline with the parser.
    #
    QDiscParser.register_qdisc('pfifo', PFifoQDisc)


The steps to add support for a new queuing discipline are:

#. Creation of a new Python class that inherits from :class:`QDisc`;
   the convention is to name such a class ``xxxQDisc``
   where ``xxx`` is the name of the queuing discipline

#. The ``xxxQDisc`` class **must** implement the
   :meth:`qdisc_creation_args` method;
   this method should return the queuing discipline-specific
   **tc(8)** arguments for creating the queuing discipline

#. The ``xxxQDisc`` class **must** implement the class method
   :meth:`parse` to create an ``xxxQDisc`` instance from a line
   of **tc(8)** output encapsulated in a :class:`QDiscOutput` instance

#. The ``xxxQDisc`` class **must** be registered by invoking the
   :meth:`QDiscParser.register_qdisc` method.

#. The ``xxxQDisc`` class **should** implement the method
   :meth:`get_description` 

#. The :meth:`__init__` method of ``xxxQDisc`` **should** take as arguments
   the particular parameters of the new queuing discipline

#. The ``xxxQDisc`` class **should** provide getter methods for the
   particular parameters of the queuing discipline

The argument to the ``xxxQDisc.parse()`` method is
a :class:`QDiscOutput` instance which contains the **unparsed** portion of
the ``qdisc`` line and zero or more lines holding qdisc statistics.
For example::

    qdisc sfq 103: parent 1:103 limit 127p quantum 1500b perturb 10sec 

The line has already already been parsed up to and including the
``parent 1:103`` field; the rest of the line is specific to the
queuing discipline. The ``xxxQDisc.parse()`` method is responsible for
parsing those fields starting with ``limit``. An iterator over those
fields can be obtained by invoking the :meth:`QDiscOutput.get_field_iter`
method.



Supporting a classful queuing discipline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the queuing discipline is classful then
in addition to the creation of a Python class for the queuing discipline,
a new Python class will also be needed
to represent the queuing class. The steps are as follows:

#. Creation of a new Python class that inherits from :class:`QClass`;
   the convention is to name such a class ``xxxQClass``
   where ``xxx`` is the name of the queuing discipline

#. The ``xxxQClass`` class **must** implement the method
   :meth:`qclass_creation_args`;
   this method should return the queuing class-specific
   **tc(8)** arguments for creating a class of the queuing discipline
   (example: :meth:`HTBQClass.qclass_creation_args`)

#. The ``xxxQDisc`` class **must** implement the class method
   :meth:`parse` to create an ``xxxQClass`` instance from a line
   of **tc(8)** output encapsulated in a :class:`QClassOutput` instance

#. The ``xxxQClass`` class **must** be registered by invoking the
   :meth:`QClassParser.register_qclass` method.

#. The ``xxxQClass`` class **should** implement the method
   :meth:`get_description` 
   (example: :meth:`HTBQClass.get_description`)

#. The :meth:`__init__` method of ``xxxQClass`` should take as arguments
   the particular parameters of the queuing class

#. The ``xxxQClass`` class **should** provide getter methods for the
   particular parameters of the queuing class

The argument to the ``xxxQDisc.parse()`` method is
a :class:`QClassOutput` instance which contains the **unparsed** portion of
the ``class`` line and zero or more lines holding class statistics.
For example::

    class htb 1:1 root rate 2000Kbit ceil 2000Kbit burst 5000b cburst 5000b 

The line has already already been parsed up to and including the
``root`` field; the rest of the line is specific to the
queuing class. The ``xxxQClass.parse()`` method is responsible for
parsing those fields starting with ``rate``. An iterator over those
fields can be obtained by invoking the :meth:`QClassOutput.get_field_iter`
method.

If the queuing discipline is classful **and** its classes are
generated automatically upon instantiation in the kernel (e.g.
the ``PRIO`` queuing discipline), the
:meth:`QDisc._instantiate_qdisc`
method **must** be
overriden to create the necessary subclasses of :class:`QClass` upon
successful instantiation of the queuing discipline
(see :class:`PrioQDisc` for an example).

.. currentmodule:: linuxnet.qos

Queuing statistics
~~~~~~~~~~~~~~~~~~

If the new queuing discipline (or class) reports additional statistics,
then a new class should be created to hold them. The
steps needed are as follows:

#. Creation of a new Python class that inherits from :class:`QStats`;
   the convention is to name such a class
   ``xxxQDiscStats`` (for queuing discipline statistics) or 
   ``xxxQClassStats`` (for queuing class statistics)
   where ``xxx`` is the name of the queuing discipline

#. the ``xxxQDisc`` (or ``xxxQClass``) class **must** implement the
   :meth:`get_stats` method; this method should return an instance
   of ``xxxQDiscStats`` (or ``xxxQClassStats``)

#. the ``xxxQDisc`` (or ``xxxQClass``) class **must** implement the
   :meth:`_parse_stats` method; this method should create a
   ``xxxQDiscStats`` (or ``xxxQClassStats``) instance which should
   be stored in the ``xxxQDisc`` (or ``xxxQClass``) instance.
   It should then invoke the :meth:`init_from_output` method
   of the new ``xxxQDiscStats`` (or ``xxxQClassStats``) instance

   The argument to the :meth:`_parse_stats` method is a
   :class:`LineGroupIterator` which returns
   the output lines that contain the statistics.
   This iterator is passed to the invoked :meth:`init_from_output` method.

#. the ``xxxQDiscStats`` (or ``xxxQClassStats``) class **must** implement the
   :meth:`init_from_output` method; this method
   should first invoke the :meth:`QStats.init_from_output` method
   which will parse the output lines that contain the common queuing
   discipline statistics, and then it should proceed to parse the statistics
   lines that are specific to the new queuing discipline/class

   The argument to this method is a :class:`LineGroupIterator` instance
   which provides access to the statistics lines.

-----------------------

.. currentmodule:: linuxnet.qos.extension

Python Classes
~~~~~~~~~~~~~~

QDisc
+++++

.. autoclass:: QDisc
   :show-inheritance:
   :members:
   :private-members: _instantiate_qdisc

--------------------

QClass
++++++

.. autoclass:: QClass
   :show-inheritance:
   :members:

--------------------

QNode
+++++

.. autoclass:: QNode
   :inherited-members:
   :private-members: _instantiate_qdisc

