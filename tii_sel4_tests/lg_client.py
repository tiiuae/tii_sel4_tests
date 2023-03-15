#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
from typing import List

from yaml import load, dump
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

CURR_DIR        = os.path.realpath(os.path.dirname(__file__))
TESTS_DIR       = os.path.join(CURR_DIR, 'tests')
TESTBEDS_DIR    = os.path.join(CURR_DIR, 'testbeds')
WRONG_DIR_NAMES = [ '__pycache__', ]


def parse_args() -> (argparse.Namespace, List[str]):
    parser = argparse.ArgumentParser(
                    prog='lg-client',
                    description='labgrid-client wrapper to use proper envs',
                    epilog='='*10)
    parser.add_argument('-t', '--testbed', required = True, help='testbed name, use "list" to show available testbeds')
    parser.add_argument('--strategy', default='', help='test strategy, use "list" to show available strategies')
    parser.add_argument('--usehost', action='store_true', help='use host name instead of ip address to access testbed')
    parser.add_argument('--upload', default='', help='upload image to testbed, both testbed and strategy need to be provided')

    return parser.parse_known_args()

def get_available_strategies() -> List[str]:
    dirs = [x for x in os.walk(TESTS_DIR)][0][1]
    return [d for d in dirs if not d in WRONG_DIR_NAMES]

def get_available_testbeds() -> List[str]:
    dirs = [x for x in os.walk(TESTBEDS_DIR)][0][1]
    return [d for d in dirs if not d in WRONG_DIR_NAMES]

def main():
    args, lg_args = parse_args()

    if args.testbed == 'list':
        print("available testbeds: ", get_available_testbeds())
        exit(0)

    if args.strategy == 'list':
        print("available strategies: ", get_available_strategies())
        exit(0)

    if args.testbed in get_available_testbeds():
        testbed_dir = os.path.join(TESTBEDS_DIR, args.testbed)
        sys.path.append(testbed_dir)
        import testbed
        testbed.init(**vars(args))
    else:
        print(f'Unknown testbed: {args.testbed}, available testbeds: {get_available_testbeds()}')
        exit(1)
    
    if args.strategy in get_available_strategies():
        strategy_path = os.path.join(TESTS_DIR, args.strategy)
        test_env_dir = os.path.join(strategy_path, 'test_env')
        sys.path.append(test_env_dir)
        import testenv
        testenv.init(**vars(args))
    elif args.strategy == '':
        pass
    else:
        print(f'Unknown strategy: {args.strategy}, available strategies: {get_available_strategies()}')
        exit(1)

    if args.upload:
        from tii_sel4_tests.utils.scp import upload

        subprocess.run(['labgrid-client env > /tmp/env_bodooboo.yaml'], shell=True).check_returncode()

        data = load(open('/tmp/env_bodooboo.yaml'), Loader=Loader)
        resources = data['targets']    \
                    .get(args.testbed) \
                    .get('resources')

        #TODO: add port here?
        host = [i for i in resources if 'NetworkService' in i.keys()][0]['NetworkService']['address']
        tftp = [i for i in resources if 'RemoteTFTPProvider' in i.keys()][0]['RemoteTFTPProvider']['internal']

        print(f"upload({args.upload}, {host}, {tftp})")
        upload(args.upload, host, tftp)
        exit(0)

    test_cmd = 'labgrid-client ' + ' '.join(lg_args)
    print(test_cmd)
    ret = subprocess.run([test_cmd], shell=True).returncode

    exit(ret)
