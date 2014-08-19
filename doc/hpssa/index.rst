hpssa module
============

Example::

    # cat raid_configuration.json
    {
        "logical_disks": [
            {
                "size_gb": 100,
                "raid_level": "1",
                "controller": "Smart Array P822 in Slot 2",
                "physical_disks": [
                    "5I:1:1",
                    "5I:1:2"
                ]
            },
            {
                "size_gb": 100,
                "raid_level": "5",
                "controller": "Smart Array P822 in Slot 2",
                "physical_disks": [
                    "5I:1:3",
                    "5I:1:4",
                    "6I:1:5"
                ]
            }
        ]
    }

    # python
    Python 2.7.5 (default, Nov  3 2014, 14:26:24)
    [GCC 4.8.3 20140911 (Red Hat 4.8.3-7)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import json
    >>> raid_config = json.loads(open('raid_configuration.json', 'r').read())
    >>> from proliantutils.hpssa import manager
    >>> manager.get_configuration()
    {'logical_disks': []}
    >>> manager.create_configuration(raid_config)
    >>> manager.get_configuration()
    {'logical_disks': [{'size_gb': 100, 'physical_disks': ['5I:1:3', '6I:1:5', '5I:1:4'], 'raid_level': '5', 'root_device_hint': {'wwn': '600508B1001C9F62EB256593E19BBA30'}, 'controller': 'Smart Array P822 in Slot 2', 'volume_name': '061D6735PDVTF0BRH5T0MO4682'}, {'size_gb': 100, 'physical_disks': ['5I:1:1', '5I:1:2'], 'raid_level': '1', 'root_device_hint': {'wwn': '600508B1001C59DB9584108610B04BB0'}, 'controller': 'Smart Array P822 in Slot 2', 'volume_name': '021D672FPDVTF0BRH5T0MO287A'}]}
    >>> exit
    Use exit() or Ctrl-D (i.e. EOF) to exit
    >>> exit()
    # ls /dev/sd*
    /dev/sda  /dev/sdb
    # python
    Python 2.7.5 (default, Nov  3 2014, 14:26:24)
    [GCC 4.8.3 20140911 (Red Hat 4.8.3-7)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from proliantutils.hpssa import manager
    >>> manager.delete_configuration()
    >>> manager.get_configuration()
    {'logical_disks': []}
    >>>
    # ls /dev/sd*
    ls: cannot access /dev/sd*: No such file or directory
    #



