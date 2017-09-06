# -*- coding: utf-8 -*-

version_major=4
version_minor=6
version_micro=0
version_extra = ''

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
__version__ = '%s.%s.%s%s' % (version_major,
                              version_minor,
                              version_micro,
                              version_extra)

# Main setup parameters
PROJECT = 'spm'  # Needed by BV
NAME = 'spm'
LICENSE = 'CeCILL-v2'
VERSION = __version__
