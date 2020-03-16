# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed

class Masking(object):
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setContrastIndexList(self, contrast_index_list):
    self.contrast_index_list = contrast_index_list

  def setMaskThreshold(self, threshold_value):
    if isinstance(threshold_value, int) or isinstance(threshold_value, float):
      self.mask_threshold_value = threshold_value
    else:
      raise ValueError('Threshold value must be "int" or "float" type, not : ' + str(type(threshold_value)))

  def setNatureOfMaskToInclusive(self):
    self.nature_of_mask = 0

  def setNatureOfMaskToExclusive(self):
    self.nature_of_mask = 1

  def getStringListForBatch( self ):
    if not None in [self.contrast_index_list, self.mask_nature]:
      if len(self.contrast_index_list) == 1:
        contrast_str = str(self.contrast_index_list[0])
      else:
        contrast_str_list = [str(contrast) for contrast in self.contrast_index_list]
        contrast_str = '[' + ' '.join(contrast_str_list) + ']'
      batch_list = []
      batch_list.append("contrasts = %s;" % contrast_str)
      batch_list.append("thresh = %g;" % self.mask_threshold_value)
      batch_list.append("mtype = %i;" % self.mask_nature)
      return batch_list
    else:
      raise ValueError('Unvalid contrast query masking, contrast index list and/or mask nature not found')
