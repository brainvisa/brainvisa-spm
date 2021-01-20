# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.stats.results_report.masking import Masking
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

class MaskingContainer(object):
  @checkIfArgumentTypeIsAllowed(Masking, 1)
  def setMasking(self, masking):
    self.masking = masking

  def disableMasking(self):
    self.masking = None

  def getStringListForBatch( self ):
    if self.masking is not None:
      batch_list = addBatchKeyWordInEachItem("mask", self.masking.getStringListForBatch())
    else:
      batch_list = ["mask = struct('contrasts', {}, 'thresh', {}, 'mtype', {});"]
    return batch_list
      
    

