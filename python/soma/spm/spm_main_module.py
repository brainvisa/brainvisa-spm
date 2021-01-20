from __future__ import absolute_import
import abc

class SPMMainModule(object):
  def __init__(self):
    raise NotImplementedError()

  def _moveSPMDefaultPathsIfNeeded(self):
    """Virtual method, redefined in subclass if necessary"""
    pass
#===============================================================================
# 
#===============================================================================
class SPM8MainModule(SPMMainModule):
  pass

#=============================================================================
# 
#=============================================================================
class SPM12MainModule(SPMMainModule):
  pass

