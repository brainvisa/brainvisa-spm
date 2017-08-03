# -*- coding: utf-8 -*-
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

class CovariateContainer():

  def getStringListForBatch( self ):
    if len(self) > 1:
      batch_list = []
      for covariate_index, covariate in enumerate(self):
        batch_list.extend(addBatchKeyWordInEachItem("cov(%s)" % (covariate_index+1), covariate.getStringListForBatch()))
    elif len( self ) == 1:
        batch_list = addBatchKeyWordInEachItem("cov", self[0].getStringListForBatch())
    else:
      batch_list = ["cov = struct('c', {}, 'cname', {}, 'iCFI', {}, 'iCC', {});"]
    return batch_list
