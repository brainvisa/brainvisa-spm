import abc

class SPMMainModule():
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

