# -*- coding: utf-8 -*-
from soma.spm.spm8.stats.contrast_manager.contrast import Contrast
from soma.spm.virtual_spm.stats.contrast_manager.fcontrast import FContrast as FContrast_virtual
from soma.spm.virtual_spm.stats.contrast_manager.fcontrast import FContrastVector as FContrastVector_virtual
from soma.spm.virtual_spm.stats.contrast_manager.fcontrast import FContrastVectorContainer as FContrastVectorContainer_virtual

class FContrast(FContrast_virtual, Contrast):
  def __init__(self):
    self.possible_options = {'Do not replicate':'none',
                             'Replicate average':'repl',
                             'Replicate no averaging':'replna',
                             'Create per session':'sess',
                             'Replicate average and Create per session':'both',
                             }
    self.replicate_over_sessions = 'none'
    self.f_contrast_vector_container = FContrastVectorContainer()
#==============================================================================
#
#==============================================================================
class FContrastVector(FContrastVector_virtual):
  def __init__(self):
    self.contrast_vector= None
#==============================================================================
#
#==============================================================================
class FContrastVectorContainer(FContrastVectorContainer_virtual):
  def __init__(self):
    self.f_contrast_vector_list = []
