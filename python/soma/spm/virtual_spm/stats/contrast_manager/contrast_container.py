# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.stats.contrast_manager.contrast import Contrast
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem


class ContrastContainer(object):
  """
  For  general  linear  model  Y  =  XB  +  E with data Y, desgin matrix X, parameter
  vector  B,  and  (independent)  errors  E,  a contrast is a linear combination of the
  parameters  c'B.  Usually  c  is  a column vector, defining a simple contrast of the
  parameters,  assessed  via  an  SPM{T}.  More generally, c can be a matrix (a linear
  constraining matrix), defining an "F-contrast" assessed via an SPM{F}.
  The  vector/matrix  c  contains  the  contrast  weights. It is this contrast weights
  vector/matrix  that  must be specified to define the contrast. The null hypothesis
  is  that  the  linear  combination  c'B  is  zero.  The order of the parameters in the
  parameter  (column)  vector  B,  and  hence  the  order  to  which  parameters are
  referenced  in the contrast weights vector c, is determined by the construction of
  the design matrix.
  """
  def getStringListForBatch( self ):
    batch_list = []
    if len(self) == 0:
      batch_list = ['consess = {};']
    else:
      for contrast_index, contrast in enumerate(self):
        key_word_contrast =  'consess' + '{' + str(contrast_index + 1) + '}'
        batch_list.extend(addBatchKeyWordInEachItem(key_word_contrast, contrast.getStringListForBatch()))
    return batch_list
