# -*- coding: utf-8 -*-
from soma.spm.spm_container import SPMContainer
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
from soma.spm.spm12.util.deformations.output import Output

class OutputContainer(SPMContainer):
  def __init__(self):
    SPMContainer.__init__(self, Output)
    
  def getStringListForBatch( self ):
    batch_list = []
    if len(self) == 0:
      batch_list.append('out = cell(1, 0);')
    else:
      for output_index, output in enumerate(self):
        key_word_output =  'out' + '{' + str(output_index + 1) + '}'
        batch_list.extend(addBatchKeyWordInEachItem(key_word_output, output.getStringListForBatch()))
    return batch_list
  
  def _moveSPMDefaultPathsIfNeeded(self):
    for output in self:
      output._moveSPMDefaultPathsIfNeeded()