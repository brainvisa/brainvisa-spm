# -*- coding: utf-8 -*-
from soma.spm.spm12.util.image_calculator.additional_variable import AdditionalVariable
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

from soma.spm.spm_container import SPMContainer

class AdditionalVariableContainer(SPMContainer):
  def __init__(self):
    SPMContainer.__init__(self, AdditionalVariable)

  def getStringListForBatch( self ):
    if len(self) > 1:
      batch_list = []
      for variable_index, variable in enumerate(self):
        batch_list.extend(addBatchKeyWordInEachItem("var(%s)" % (variable_index+1), variable.getStringListForBatch()))
    elif len( self ) == 1:
        batch_list = addBatchKeyWordInEachItem("var", self[0].getStringListForBatch())
    else:
      batch_list = ["var = struct('name', {}, 'value', {});"]
    return batch_list