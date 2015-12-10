# Copyright 2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import print_function
import logging
import threading
import time
import timeit

from oslo_utils import importutils


ilo_client = importutils.try_import('proliantutils.ilo.client')
ilo_error = importutils.try_import('proliantutils.exception')
ilo_new_client = importutils.try_import('proliantutils.ilo.client_new')

LOG_FILENAME = 'log.out'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,)

LOG = logging.getLogger("test_ilo")


driver_info = {"ilo_address": "10.10.1.57",
               "ilo_username": "administrator",
               "ilo_password": "12iso*help",
               "client_timeout": 60,
               "client_port":  443
               }


METHOD_LIST = ["get_product_name", "get_host_power_status",
               "get_one_time_boot", "get_current_boot_mode",
               "get_supported_boot_mode"]


def get_ilo_object():
    ilo_object = ilo_client.IloClient(driver_info['ilo_address'],
                                      driver_info['ilo_username'],
                                      driver_info['ilo_password'],
                                      driver_info['client_timeout'],
                                      driver_info['client_port'])
    return ilo_object


def get_new_ilo_object():
    ilo_object = ilo_new_client.IloClient(driver_info['ilo_address'],
                                          driver_info['ilo_username'],
                                          driver_info['ilo_password'],
                                          driver_info['client_timeout'],
                                          driver_info['client_port'])
    return ilo_object

ILO_VARIANTS = {"old": get_ilo_object,
                "new": get_new_ilo_object
                }

setup = lambda var_type: "from __main__ import %s,run_funcs" % (
                         ILO_VARIANTS[var_type].__name__)


def run_funcs(var_type):
    for i in METHOD_LIST:
        ilob = ILO_VARIANTS[var_type]()
        if hasattr(ilob, i):
            LOG.info("%s : Running %s :" % (var_type, i))
            getattr(ilob, i)()

print ("################################################################")
print ("Test case - 1")
print ("    This test case runs the 5 ILO operations on both code flows ")
print ("    for 3 times and derives the results.")
print ("################################################################")
for i in ILO_VARIANTS:
    print ("\tRunning test on %s code flow" % i)
    print ("\t=============================")
    print ("\t", timeit.timeit('run_funcs("%s")' % i, setup=setup(i),
           number=3), "\n")

print ("################################################################")
print ("Test case - 2")
print ("    This test case runs the 5 ILO operations on both code flows ")
print ("    for 3 times and derives the results.")
print ("################################################################")

print ("\tRunning test on new code flow")
print ("\t=============================")
t1 = time.time()
tds = []
for td in range(5):
    ot = threading.Thread(target=run_funcs, args=("new",))
    tds.append(ot)
    ot.start()

for tid in tds:
    tid.join()

t2 = time.time()

print ("Executeed in %d seconds" % (t2-t1))
print ("\tRunning test on old code flow")
print ("\t=============================")
t1 = time.time()
tds = []
for td in range(5):
    ot = threading.Thread(target=run_funcs, args=("old",))
    tds.append(ot)
    ot.start()

for tid in tds:
    tid.join()

t2 = time.time()

print ("Executeed in %d seconds" % (t2-t1))
