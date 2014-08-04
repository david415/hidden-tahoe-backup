## this setup.py was inspired by Meejah's txtorcon setup.py
## https://github.com/meejah/txtorcon

try:
    import pypissh
except:
    print "WARNING: not using PyPi over SSH!"
import sys
import os
import os.path
import shutil
import re
from distutils.core import setup

__version__ = '0.0.1'
__author__ = 'David Stainton'
__contact__ = 'dstainton415@gmail.com'
__url__ = 'https://github.com/david415/hidden-tahoe-backup'
__license__ = 'GPL'
__copyright__ = 'Copyright 2014'


def pip_to_requirements(s):
    """
    Change a PIP-style requirements.txt string into one suitable for setup.py
    """

    if s.startswith('#'):
        return ''
    m = re.match('(.*)([>=]=[.0-9]*).*', s)
    if m:
        return '%s (%s)' % (m.group(1), m.group(2))
    return s.strip()

setup(name = 'hiddenTahoeBackup',
      version = __version__,
      description = 'Clandestine Tahoe-LAFS backup system for Tails with Twisted-PyGTK+3 and CLI interfaces',
      long_description = open('README.md', 'r').read(),
      keywords = ['python', 'twisted', 'tor', 'tahoe-lafs'],
      ## way to have "development requirements"?
      requires = filter(len, map(pip_to_requirements, open('requirements.txt').readlines())),
      ## FIXME is requires even doing anything? why is format
      ## apparently different for install_requires?
      install_requires = ['Twisted>=14.0.0', 'cffi', 'pynacl'],
      classifiers = ['Framework :: Twisted',
                     'Development Status :: Alpha',
                     'Intended Audience :: Users',
                     'License :: OSI Approved :: GPL License',
                     'Natural Language :: English',
                     'Operating System :: POSIX :: Linux',
                     'Operating System :: Unix',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2',
                     'Programming Language :: Python :: 2.6',
                     'Programming Language :: Python :: 2.7',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'Topic :: Internet',
                     'Topic :: Security'],
      author = __author__,
      author_email = __contact__,
      url = __url__,
      license = __license__,
      packages = ["HiddenTahoeBackup"],
      package_dir={'HiddenTahoeBackup': 'HiddenTahoeBackup'},
      scripts = ['HiddenTahoeBackup/secretBox.py',
                 'HiddenTahoeBackup/hiddenBackupCLI.py',
                 'HiddenTahoeBackup/hiddenBackupGTK.py'],
      data_files = [('share/HiddenTahoeBackup', ['README.md'])],
      )

