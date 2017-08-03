# -*- coding: utf-8 -*-

from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
import numpy

class FContrast():
  """
  * Linear constraining matrices for an SPM{F}
  The  null  hypothesis  c'B=0  can  be thought of as a (linear) constraint on the full
  model  under  consideration,  yielding a reduced model. Taken from the viewpoint
  of  two  designs,  with  the full model an extension of the reduced model, the null
  hypothesis is that the additional terms in the full model are redundent.
  Statistical  inference  proceeds  by comparing the additional variance explained by
  full  design  over  and  above  the reduced design to the error variance (of the full
  design),  an  "Extra  Sum-of-Squares"  approach  yielding  an  F-statistic for each
  voxel, whence an SPM{F}.
  """
  def appendFContrastVector(self, f_contrast_vector):
    self.f_contrast_vector_container.appendFContrastVector(f_contrast_vector)

  def setFContrastVectorList(self, f_contrast_vector_list):
    self.f_contrast_vector_container.setFContrastVectorList(f_contrast_vector_list)

  def clearFContrastVectorList(self):
     self.f_contrast_vector_container.clearFContrastVectorList()

  def setReplicateOverSessions(self, option):
    """
    If there are multiple sessions with identical conditions, one might want to specify
    contrasts which are identical over sessions. This can be done automatically based
    on the contrast spec for one session.
    Contrasts  can be either replicated (either testing average effects over sessions or
    per-session/condition   effects)   or  created  per  session.  In  both  cases,  zero
    padding   up   to   the  length  of  each  session  and  the  block  effects  is  done
    automatically.
    """
    if option in self.possible_options.keys():
      self.replicate_over_sessions = self.possible_options[option]
    else:
      raise ValueError('Replicate over sessions possibilities are : ' + str(self.possible_options.keys()))
 
  def getStringListForBatch( self ):
    if self.name is not None:
      batch_list = []
      batch_list.append("fcon.name = '%s';" % self.name)
      batch_list.append("fcon.sessrep = '%s';" % self.replicate_over_sessions)
      batch_list.extend(addBatchKeyWordInEachItem("fcon",self.f_contrast_vector_container.getStringListForBatch()))
      return batch_list
    else:
      raise ValueError('Unvalid contrast, name or array not found')
    
#==============================================================================
#
#==============================================================================
class FContrastVector():
  @checkIfArgumentTypeIsAllowed(numpy.ndarray, 1)
  def setFContrastVector(self, numpy_array):
    self.contrast_vector= numpy_array

  def getArrayForBatchScript( self):
    if self.contrast_vector is not None:
      return self._createArrayForBatchScript()

  def _createArrayForBatchScript(self):
    array_str_list = []
    if len(self.contrast_vector.shape) == 1:
      coeff_list = [str(coeff) for coeff in self.contrast_vector]
      array_str_list.append(' '.join(coeff_list))
    else:
      for row in self.contrast_vector:
        row_coeff_list = [str(coeff) for coeff in row]
        array_str_list.append(' '.join(row_coeff_list))
    array_str = '[' + '\n'.join(array_str_list) + ']\n'
    return array_str
#==============================================================================
#
#==============================================================================
class FContrastVectorContainer():
  @checkIfArgumentTypeIsAllowed(FContrastVector, 1)
  def appendFContrastVector(self, f_contrast_vector):
    self.f_contrast_vector_list.append(f_contrast_vector)

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setFContrastVectorList(self, f_contrast_vector_list):
    self.f_contrast_vector_list = []
    for f_contrast_vector in f_contrast_vector_list:
      self.f_contrast_vector_list.append(f_contrast_vector)

  def clearFContrastVectorList(self):
    self.f_contrast_vector_list = []
 
  def getStringListForBatch( self ):
    batch_list = []
    array_str = ''
    for f_contrast_vector in self.f_contrast_vector_list:
      array_str += f_contrast_vector.getArrayForBatchScript()
    batch_list.append("convec = {\n%s}';" % array_str)
    return batch_list
    

