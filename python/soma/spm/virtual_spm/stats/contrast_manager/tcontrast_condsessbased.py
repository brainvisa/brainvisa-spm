# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

import numbers
class TContrastCondSessBased(object):
  """
  Define  a  contrast in terms of conditions or regressors instead of columns of the
  design   matrix.   This  allows  to  create  contrasts  automatically  even  if  some
  columns are not always present (e.g. parametric modulations).
  """
  @checkIfArgumentTypeIsAllowed(list,1)
  def setSessionVector(self, session_vector):
    """
    Enter  session  number(s)  for which this contrast should be created. If more than
    one session number is specified, the contrast will be an average contrast over the
    specified conditions or regressors from these sessions.
    """
    self.session_vector = session_vector
#==============================================================================
#
#==============================================================================
class TContrastCondSessBasedWithExtraRegressors(object):
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setVector(self, vector):
    self.vector = vector
  
  def getStringListForBatch( self ):
    if self.vector and not None in [self.session_vector, self.name]:
      vector_list = [str(coeff) for coeff in self.vector]
      vector_str = ' '.join(vector_list)
  
      vector_session_list = [str(coeff) for coeff in self.session_vector]
      vector_session_str = ' '.join(vector_session_list)
      
      batch_list = []
      batch_list.append("tconsess.name = '%s';" % self.name)
      batch_list.append("tconsess.colreg = [%s];" % vector_str)
      batch_list.append("tconsess.sessions = [%s];" % vector_session_str)
      return batch_list
    else:
      raise ValueError('Empty TContrast for extra regressors vector')
#==============================================================================
#
#==============================================================================
class TContrastCondSessBasedWithConditions(object):
  def appendContrastEntry(self, contrast_entry):
    self.contrast_entry_container.appendContrastEntry(contrast_entry)

  def setContrastEntryList(self, contrast_entry_list):
    self.contrast_entry_container.setContrastEntryList(contrast_entry_list)

  def clearContrastEntryList(self):
    self.contrast_entry_container.clearContrastEntryList()
  
  def getStringListForBatch( self ):
    vector_session_list = [str(coeff) for coeff in self.session_vector]
    vector_session_str = ' '.join(vector_session_list)

    batch_list = []
    batch_list.append("tconsess.name = '%s';" % self.name)
    batch_list.append("tconsess.sessions = [%s];" % vector_session_str)
    batch_list.extend(addBatchKeyWordInEachItem("tconsess", self.contrast_entry_container.getStringListForBatch()))
    return batch_list
#==============================================================================
class ContrastEntry(object):
  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
  def setContrastWeight(self, contrast_weight):
    self.contrast_weight = contrast_weight

  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
  def setCondition(self, condition):
    self.condition = condition

  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
  def setBasisFunction(self, basis_function):
    self.basis_function = basis_function

  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
  def setParametricModulation(self, parametric_modulation):
    self.parametric_modulation = parametric_modulation

  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
  def setParametricModulationOrder(self, parametric_modulation_order):
    self.parametric_modulation_order = parametric_modulation_order
 
  def getStringListForBatch( self ):
    if not None in [self.contrast_weight,
                    self.condition,
                    self.basis_function,
                    self.parametric_modulation,
                    self.parametric_modulation_order]:
      batch_list = []
      batch_list.append("conweight = %g;" % self.contrast_weight)
      batch_list.append("colcond = %g;" % self.condition)
      batch_list.append("colbf = %g;" % self.basis_function)
      batch_list.append("colmod = %g;" % self.parametric_modulation)
      batch_list.append("colmodord = %g;" % self.parametric_modulation_order)
      return batch_list
    else:
      raise ValueError('Unvalid contrast Entry, one or more argument not found')
#==============================================================================
class ContrastEntryContainer(object):
  @checkIfArgumentTypeIsAllowed(ContrastEntry, 1)
  def appendContrastEntry(self, contrast_entry):
    self.contrast_entry_list.append(contrast_entry)

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setContrastEntryList(self, contrast_entry_list):
    self.contrast_entry_list = []
    for contrast_entry in contrast_entry_list:
      self.appendContrastEntry(contrast_entry)

  def clearContrastEntryList(self):
    self.contrast_entry_list = []

  def getStringListForBatch( self ):
    batch_list = []
    if len(self.contrast_entry_list) == 0:
      batch_list.append("tconsess.coltype.colconds = struct('conweight', {}, 'colcond', {}, 'colbf', {}, 'colmod', {}, 'colmodord', {});")
    elif len(self.contrast_entry_list) == 1:
      batch_list.extend(addBatchKeyWordInEachItem('tconsess.coltype.colconds',
                                                  self.contrast_entry_list[0].getStringListForBatch()))
    elif len(self.contrast_entry_list) > 1:
      for contrast_entry_index, contrast in enumerate(self.contrast_entry_list):
        key_word_contrast =  'tconsess.coltype.colconds' + '(' + str(contrast_entry_index + 1) + ')'
        batch_list.extend(addBatchKeyWordInEachItem(key_word_contrast, contrast.getStringListForBatch()))
    return batch_list
