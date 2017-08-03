# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.stats.results_report.contrast_query import ContrastQuery as ContrastQuery_virtual
from soma.spm.spm12.stats.results_report.masking import Masking

from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed

class ContrastQuery(ContrastQuery_virtual):
  def __init__(self):
    self.title = ''
    self.contrast_index_list = None
    self.threshold_type = 'FWE'
    self.threshold_value = 0.05
    self.extent_value = 0
    self.masking = None

  def unsetMasking(self):
    self.masking = None

  @checkIfArgumentTypeIsAllowed(Masking, 1)
  def setMasking(self, masking):
    self.masking = masking

  def disableMasking(self):
    raise NotImplementedError("it is deprecated in SPM12")

  def getStringListForBatch( self ):
    if self.contrast_index_list is not None:
      batch_list = []
      batch_list.append("titlestr = '%s';" % self.title)
      if len(self.contrast_index_list) == 1:
        contrast_str = str(self.contrast_index_list[0])
      else:
        contrast_str_list = [str(contrast) for contrast in self.contrast_index_list]
        contrast_str = '[' + ' '.join(contrast_str_list) + ']'
      batch_list.append("contrasts = %s;" % contrast_str)
      batch_list.append("threshdesc = '%s';" % self.threshold_type)
      batch_list.append("thresh = %s;" % self.threshold_value)
      batch_list.append("extent = %s;" % self.extent_value)
      if self.masking is not None:
        batch_list.extend(self.masking.getStringListForBatch())
      else:
        batch_list.append("mask.none = 1;")
      return batch_list
    else:
      raise ValueError('Unvalid contrast query, contrast index list not found')
