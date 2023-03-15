#!/usr/bin/env python

from setuptools import setup

def get_requirements():
    with open('requirements.txt') as f:
        packages = []
        for line in f:
            line = line.strip()
            # let's also ignore empty lines and comments
            if not line or line.startswith('#'):
                continue
            packages.append(line)
    return packages

REQUIRES = get_requirements()

with open("README.md", "r") as fh:
    long_description = fh.read()



setup(name='tii_sel4_tests',
      version='0.1',
      license='',
      description='TII seL4 automation tests',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/tiiuae/tii_sel4_tests',
      keywords = ['TII', 'seL4', 'labgrid', 'pytest', 'ci\\cd'],
      packages=['tii_sel4_tests'],
      package_dir={'tii_sel4_tests': 'tii_sel4_tests'},
      package_data={'tii_sel4_tests': [
          'tests/**/**/*.py',
          'tests/**/**/*.yaml',
          'tests/**/*.py',
          'tests/*.py',
          'testbeds/**/*.py',
          'utils/*.py',
          ]},
      python_requires='>=3.7',
      install_requires=REQUIRES,
      entry_points = {
        'console_scripts': [
            'run_tests=tii_sel4_tests.run_tests:main',
            'lg_client=tii_sel4_tests.lg_client:main',
        ],
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Topic :: Test Automation',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
      ],
)
