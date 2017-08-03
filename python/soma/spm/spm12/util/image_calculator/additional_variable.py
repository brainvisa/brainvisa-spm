# -*- coding: utf-8 -*-
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
from soma.spm.spm_batch_maker_utils import convertNumpyArrayToSPMString
import numpy

class AdditionalVariable():
  """
  Additional variable which can be used in expression.
  """
  def __init__(self):
    self.name = None
    self.value = None
  
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setName(self, name):
    """
    Variable name used in expression.
    """
    self.name = name
  
  @checkIfArgumentTypeIsAllowed(numpy.ndarray, 1)  
  def setValue(self, numpy_array):
    """
    Value of the variable.
    """
    self.value = convertNumpyArrayToSPMString(numpy_array)
    
  def getStringListForBatch( self ):
    batch_list = []
    batch_list.append("name = '%s';" %self.name)
    batch_list.append("value = %s;" %self.value)
    return batch_list