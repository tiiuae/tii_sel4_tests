import os
from tii_sel4_tests.utils.testbed import Testbed

def init(*args, **kwargs) -> None:
    testbed = {
        'name': 'sqa1',
        'crossbar_ip': '172.18.8.169',
        'crossbar_hostname': 'sqa1' if kwargs['usehost'] else '',
        'proxy_ip': '172.18.8.169',
        'proxy_hostname': 'sqa1' if kwargs['usehost'] else '',
    }

    tb = Testbed(**testbed)
    return tb
