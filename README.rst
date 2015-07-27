proliantutils
=============

**proliantutils** is a set of utility libraries for interfacing and managing
various components (like iLO, HPSSA) for HP Proliant Servers.  This library
is used by iLO drivers in Ironic for managing Proliant Servers (though the
library can be used by anyone who wants to manage HP Proliant servers).

Please use launchpad_ to report bugs and ask questions.

.. _launchpad: https://bugs.launchpad.net/proliantutils

Installation
------------

Install the module from PyPI_.  If you are using Ironic, install the module
on Ironic conductor node::

  pip install proliantutils

.. _PyPI: https://pypi.python.org/pypi/proliantutils

Some GNU/Linux distributions provide *python-proliantutils* package.

Usage
-----

iLO
~~~

For interfacing with the iLO, use *IloClient* object::

  >>> from proliantutils.ilo import client
  >>> ilo_client = client.IloClient('10.10.1.57', 'Administrator', 'password')
  >>> ilo_client.get_host_power_status()
  'OFF'
  >>>

For operations supported on the client object, please refer
*proliantutils.ilo.operations*.
