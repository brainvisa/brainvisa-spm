# -*- coding: utf-8 -*-
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

class SimpleContrastContainer():
  
  def getStringListForBatch( self ):
    batch_list = []
    if len(self) == 1:
      batch_list.extend(addBatchKeyWordInEachItem("gcon", self[0].getStringListForBatch()))
    elif len(self) > 1:
      for simple_contrast_index, simple_contrast in enumerate(self):
        batch_list.extend(addBatchKeyWordInEachItem("gcon(%i)" % (simple_contrast_index+1), simple_contrast.getStringListForBatch()))
    else:
      batch_list.append("gcon = struct('name', {}, 'convec', {});")
    return batch_list
        
