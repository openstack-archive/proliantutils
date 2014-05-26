==============
Proliant Utils
==============

Proliant Management Tools provides python libraries for interfacing and 
managing various devices(like iLO) present in HP Proliant Servers.

Currently, this module offers a library to interface to iLO4 using RIBCL.

```python
#!/usr/bin/python

from proliantutils.ilo import ribcl

ilo_client = ribcl.IloClient('1.2.3.4', 'Administrator', 'password')
print ilo_client.get_host_power_status()
```

Currently, this module offers only a single unit test library:

```
$ python -m unittest proliantutils.tests.ilo.test_ribcl
................
----------------------------------------------------------------------
Ran 16 tests in 0.649s

OK
$
```

