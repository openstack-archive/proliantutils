import timeit
import time
import logging
from oslo_utils import importutils
from threading import Thread


ilo_client = importutils.try_import('proliantutils.ilo.client')
ilo_error = importutils.try_import('proliantutils.exception')
ilo_new_client = importutils.try_import('proliantutils.ilo.client_new')

LOG_FILENAME = 'log.out'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,)

LOG = logging.getLogger("test_ilo")


driver_info = { 
                "ilo_address" : "10.10.1.57",
                "ilo_username": "administrator",
                "ilo_password": "12iso*help",
                "client_timeout": 60,
                "client_port":  443
              }


METHOD_LIST = [ "get_product_name","get_host_power_status",\
                "get_one_time_boot","get_current_boot_mode","get_supported_boot_mode" ]


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

ILO_VARIANTS = { 
                 "old": get_ilo_object,
                 "new": get_new_ilo_object
               }

setup = lambda var_type: "from __main__ import %s,run_funcs" % ILO_VARIANTS[var_type].__name__

def run_funcs(var_type):
    for i in METHOD_LIST:
        ilob = ILO_VARIANTS[var_type]()
        if hasattr(ilob,i):
            LOG.info("%s : Running %s :" % (var_type,i) )
            getattr(ilob,i)()

print "################################################################"
print "Test case - 1"
print "    This test case runs the 5 ILO operations on both code flows " 
print "    for 3 times and derives the results."
print "################################################################"
for i in ILO_VARIANTS:
    print "\tRunning test on %s code flow" % i
    print "\t=============================" 
    print "\t", timeit.timeit('run_funcs("%s")' % i, setup=setup(i),number=3), "\n"

print "################################################################"
print "Test case - 2"
print "    This test case runs the 5 ILO operations on both code flows " 
print "    for 3 times and derives the results."
print "################################################################"

print "\tRunning test on new code flow"
print "\t=============================" 
#sys.exit(0)
t1=time.time()
tds = []
for td in range(5):
    ot = Thread(target=run_funcs,args=("new",))
    tds.append(ot)
    ot.start()

for tid in tds:
    tid.join()

t2=time.time()

print "Executeed in %d seconds"%(t2-t1)
print "\tRunning test on old code flow"
print "\t=============================" 
t1=time.time()
tds = []
for td in range(5):
    ot = Thread(target=run_funcs,args=("old",))
    tds.append(ot)
    ot.start()

for tid in tds:
    tid.join()

t2=time.time()

print "Executeed in %d seconds"%(t2-t1)
