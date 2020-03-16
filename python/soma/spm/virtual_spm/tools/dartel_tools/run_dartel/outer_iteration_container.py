# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

class OuterIterationContainer(object):

  def getStringListForBatch( self ):
    batch_list = []
    if len(self) == 0:
      raise ValueError('At least one outer iteration is mandatory')
    elif len(self) == 1:
      batch_list.extend(addBatchKeyWordInEachItem('param', self[0].getStringListForBatch()))
    else:
      for outer_iteration_index, outer_iteration in enumerate(self):
        key_word_outer_iteration =  'param' + '(' + str(outer_iteration_index + 1) + ')'
        batch_list.extend(addBatchKeyWordInEachItem(key_word_outer_iteration, outer_iteration.getStringListForBatch()))
    return batch_list