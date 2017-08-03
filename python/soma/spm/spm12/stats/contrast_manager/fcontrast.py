# -*- coding: utf-8 -*-
from soma.spm.spm12.stats.contrast_manager.contrast import Contrast
from soma.spm.virtual_spm.stats.contrast_manager.fcontrast import FContrast as FContrast_virtual
from soma.spm.virtual_spm.stats.contrast_manager.fcontrast import FContrastVector as FContrastVector_virtual
from soma.spm.virtual_spm.stats.contrast_manager.fcontrast import FContrastVectorContainer as FContrastVectorContainer_virtual

from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.spm_batch_maker_utils import convertNumpyArrayToSPMString

import numpy

class FContrast(FContrast_virtual, Contrast):
  def __init__(self):
    self.possible_options = {'Do not replicate':'none',
                             'Replicate average':'repl',
                             'Replicate no averaging':'replna',
                             'Create per session':'sess',
                             'Replicate average and Create per session':'both',
                             }
    self.replicate_over_sessions = 'none'
    self.weights_matrix = None

  def appendFContrastVector(self, f_contrast_vector):
    raise NotImplementedError("it is deprecated in SPM12")

  def setFContrastVectorList(self, f_contrast_vector_list):
    raise NotImplementedError("it is deprecated in SPM12")

  def clearFContrastVectorList(self):
    raise NotImplementedError("it is deprecated in SPM12")

  @checkIfArgumentTypeIsAllowed(numpy.ndarray, 1)
  def setFContrastWeightsMatrix(self, numpy_array):
    self.weights_matrix= numpy_array

  def getStringListForBatch( self ):
    if self.name is not None:
      batch_list = []
      batch_list.append("fcon.name = '%s';" % self.name)
      batch_list.append("fcon.sessrep = '%s';" % self.replicate_over_sessions)
      batch_list.append("fcon.weights = %s;" % convertNumpyArrayToSPMString(self.weights_matrix))
      return batch_list
    else:
      raise ValueError('Unvalid contrast, name or array not found')
#==============================================================================
#
#==============================================================================
class FContrastVector(FContrastVector_virtual):
  def __init__(self):
    raise NotImplementedError("it is deprecated in SPM12")
#==============================================================================
#
#==============================================================================
class FContrastVectorContainer(FContrastVectorContainer_virtual):
  def __init__(self):
    raise NotImplementedError("it is deprecated in SPM12")
