# linuxnet-qos

**linuxnet-qos** provides programmatic access to the
**tc(8)** command.
Using **linuxnet-qos** one can manipulate the Linux Traffic Control
functionality (queuing disciplines).

For the following examples, Python3 (3.6 or later) is required.

Accessing an interface's queuing discipline configuration:

```python
>>> from linuxnet.qos import QDiscConfig
>>> config = QDiscConfig('eth2')
>>> config.dump()
PFifoFastQDisc(0:0) root bands 3 priomap 1 2 2 2 1 2 0 0 1 1 1 1 1 1 1 1
```

`PFifoFastQDisc` is the Python class used to represent the
`pfifo_fast` queuing discipline (see **tc-pfifo_fast(8)**).

The following examples modify the interface's queuing discipline, so
root privileges are required for successful execution of the `tc`
command.

Replacing the interface's root queuing discipline:

```python
>>> from linuxnet.qos import NetemQDisc, Handle
>>> netem_qdisc = NetemQDisc(Handle(1,1), None, delay=30.0)
>>> config.create_qdisc(netem_qdisc)
>>> config.dump()
NetemQDisc(1:1) root delay 30.0ms
```

Deleting the existing queuing discipline configuration:

```python
>>> config.delete_config()
>>> config.read_interface_config()
True
>>> config.dump()
PFifoFastQDisc(0:0) root bands 3 priomap 1 2 2 2 1 2 0 0 1 1 1 1 1 1 1 1
```

---------------------

# Installation

Python3 is required.

Available `Makefile` targets can be listed by invoking `make` with no arguments.

`make install` will install the package.

`make test` runs the unit tests.

