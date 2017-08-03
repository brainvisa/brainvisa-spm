# -*- coding: utf-8 -*-
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

class ContrastQueryContainer():

  def getStringListForBatch( self ):
    if len(self) == 1:
      batch_list = addBatchKeyWordInEachItem("conspec", self[0].getStringListForBatch())
    elif len(self) > 1:
      batch_list = [] 
      for contrast_query_index, contrast_query in enumerate(self):
        batch_list.extend(addBatchKeyWordInEachItem("conspec(%i)" % (contrast_query_index+1), contrast_query.getStringListForBatch()))
    else:
      batch_list = ["conspec = struct('titlestr', {}, 'contrasts', {}, 'threshdesc', {}, 'thresh', {}, 'extent', {}, 'mask', {});"]
    return batch_list
    
