# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed

class TContrast(object):
  """
  * Simple one-dimensional contrasts for an SPM{T}
  A  simple  contrast  for  an  SPM{T}  tests  the  null  hypothesis  c'B=0 against the
  one-sided alternative c'B>0, where c is a column vector.
      Note  that  throughout  SPM, the transpose of the contrast weights is used for
      display  and  input.  That is, you'll enter and visualise c'. For an SPM{T} this will
      be a row vector.
  """
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setVector(self, vector):
    self.vector = vector

  def setReplicateOverSessions(self, option):
    if option in list(self.possible_options.keys()):
      self.replicate_over_sessions = self.possible_options[option]
    else:
      raise ValueError('Replicate over sessions possibilities are : ' + str(list(self.possible_options.keys())))
  
  def getStringListForBatch( self ):
    if not None in [self.vector, self.name]:
      batch_list = []
      batch_list.append("tcon.name = '%s';" % self.name)
      vector_list = [str(coeff) for coeff in self.vector]
      vector_str = ' '.join(vector_list)
      batch_list.append("tcon.convec = [%s];" % vector_str)
      batch_list.append("tcon.sessrep = '%s';" % self.replicate_over_sessions)
      return batch_list
    else:
      raise ValueError('Unvalid contrast, name or vector not found')
    
