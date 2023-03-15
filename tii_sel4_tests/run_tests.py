#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
from typing import List
from datetime import datetime

CURR_DIR        = os.path.realpath(os.path.dirname(__file__))
TESTS_DIR       = os.path.join(CURR_DIR, 'tests')
TESTBEDS_DIR    = os.path.join(CURR_DIR, 'testbeds')
CURR_DATETIME   = datetime.now().strftime('%d%m%Y_%H%M')
WRONG_DIR_NAMES = [ '__pycache__', ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
                    prog='run_tests',
                    description='TII seL4 test runner',
                    epilog='='*10)
    parser.add_argument('test_name', help='test case name to be executed')
    parser.add_argument('-m', '--testmarker', default='',
            help='test marker: logdir/{test_marker}/test_name, default: current date')
    parser.add_argument('-t', '--testbed', default='sqa1', help='testbed name, default: sqa1')
    parser.add_argument('-i', '--image', help='image path to upload on testbed')
    parser.add_argument('-l', '--logdir', default='./logs', help='dir to save logs')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-w', '--vverbose', action='store_true')
    parser.add_argument('-k', '--kick', action='store_true', help='force testbed unlock (kick user)')
    parser.add_argument('--usehost', action='store_true', help='use host name instead of ip address to access testbed')

    return parser.parse_args()

def get_available_tests() -> List[str]:
    dirs = [x for x in os.walk(TESTS_DIR)][0][1]
    return [d for d in dirs if not d in WRONG_DIR_NAMES]

def get_available_testbeds() -> List[str]:
    dirs = [x for x in os.walk(TESTBEDS_DIR)][0][1]
    return [d for d in dirs if not d in WRONG_DIR_NAMES]

def prepare_test_args(test_path: str, args: argparse.Namespace) -> str:
    cmd = 'pytest '

    if args.vverbose:
        cmd += '-vv -s '
    elif args.verbose:
        cmd += '-v '

    cmd += '--lg-env $LG_ENV '
    
    logdir = os.path.join(args.logdir, args.testmarker if args.testmarker else CURR_DATETIME, args.test_name)
    cmd += f'--lg-log={logdir} '

    cmd += f'{test_path} '

    if vars(args).get('image', None):
        cmd += f'--boot-image={args.image} '

    return cmd

def main():
    args = parse_args()

    if not args.test_name in get_available_tests():
        print(f'Unknown test_name: {args.test_name}, available tests: {get_available_tests()}')
        exit(1)

    test_path = os.path.join(TESTS_DIR, args.test_name)

    if not args.testbed in get_available_testbeds():
        print(f'Unknown testbed: {args.testbed}, available testbeds: {get_available_testbeds()}')
        exit(1)

    testbed_dir = os.path.join(TESTBEDS_DIR, args.testbed)
    sys.path.append(testbed_dir)
    import testbed

    test_env_dir = os.path.join(test_path, 'test_env')
    sys.path.append(test_env_dir)
    import testenv

    testbed.init(**vars(args))
    testenv.init(**vars(args))

    subprocess.run([f'labgrid-client show'], shell=True).check_returncode()
    subprocess.run([f'labgrid-client unlock {"-k" if args.kick else ""}'], shell=True)
    subprocess.run([f'labgrid-client lock'], shell=True).check_returncode()

    test_cmd = prepare_test_args(test_path, args)
    print(test_cmd)
    ret = subprocess.run([test_cmd], shell=True).returncode

    subprocess.run([f'labgrid-client unlock'], shell=True).check_returncode()

    exit(ret)
