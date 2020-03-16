# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm_main_module import SPM8MainModule

from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode

from soma.spm.spm8.tools.vbm.estimation_options import EstimationOptions
from soma.spm.spm8.tools.vbm.extended_options import ExtendedOptions
from soma.spm.spm8.tools.vbm.writing_options import WritingOptions

class EstimateAndWrite(SPM8MainModule):
  def __init__(self):
    self.volume_path_list = None
    self.estimate_options = EstimationOptions()
    self.extended_options = ExtendedOptions()
    self.writing_options = WritingOptions(dartel_normalization=True)
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setVolumePath(self, volume_path):
    """
    Select  raw  data  (e.g. T1 images) for processing. This assumes that there is one scan for
    each  subject.  Note  that multi-spectral (when there are two or more registered images of
    different contrasts) processing is not yet implemented for this method.
    """
    self.volume_path_list = [volume_path]
     
  @checkIfArgumentTypeIsAllowed(list, 1)  
  def setVolumesPathList(self, volume_path_list):
    self.volume_path_list = volume_path_list
    
  @checkIfArgumentTypeIsAllowed(EstimationOptions, 1)  
  def replaceEstimationOptions(self, estimate_options):
    del self.estimate_options
    self.estimate_options = estimate_options
    
  @checkIfArgumentTypeIsAllowed(ExtendedOptions, 1)  
  def replaceExtendedOptions(self, extended_options):
    del self.extended_options
    self.extended_options = extended_options
    
  @checkIfArgumentTypeIsAllowed(WritingOptions, 1)  
  def replaceWritingOptions(self, writing_options):
    del self.writing_options
    self.writing_options = writing_options
    
  def getStringListForBatch(self):
    if self.volume_path_list is not None: 
      volume_path_list_for_batch = [] 
      for volume_path in self.volume_path_list:
        volume_path_list_for_batch.append("'%s,1'" % volume_path)
      volume_path_for_batch = '\n'.join(volume_path_list_for_batch)
      batch_list = []
      batch_list.append("spm.tools.vbm8.estwrite.data = {%s};" % volume_path_for_batch)
      batch_list.extend(addBatchKeyWordInEachItem("spm.tools.vbm8.estwrite", self.estimate_options.getStringListForBatch()))
      batch_list.extend(addBatchKeyWordInEachItem("spm.tools.vbm8.estwrite", self.extended_options.getStringListForBatch()))
      batch_list.extend(addBatchKeyWordInEachItem("spm.tools.vbm8.estwrite", self.writing_options.getStringListForBatch()))
      return batch_list
    else:
      raise ValueError('At least one volume path is required')
  
  def _moveSPMDefaultPathsIfNeeded(self):
    for volume_path in self.volume_path_list:
      self.writing_options.moveSPMDefaultPathsIfNeeded(volume_path)

  