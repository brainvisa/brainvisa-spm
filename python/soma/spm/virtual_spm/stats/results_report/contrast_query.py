# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode

class ContrastQuery(object):
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setTitle(self, title):
    """
    Heading on results page - determined automatically if left empty
    """
    self.title = title

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setContrastIndexList(self, contrast_index_list):
    """
    Index  of  contrast(s).  If more than one number is entered, analyse a conjunction
    hypothesis.
    """
    self.contrast_index_list = contrast_index_list

  def setThresholdToFWE(self):
    self.threshold_type = 'FWE'

  def setThresholdToFDR(self):
    self.threshold_type = 'FDR'

  def unsetThreshold(self):
    self.threshold_type = 'none'

  def setThresholdValue(self, threshold_value):
    if isinstance(threshold_value, float) or isinstance(threshold_value, int):
      self.threshold_value = threshold_value
    else:
      raise ValueError('Threshold value must be "int" or "float" type, not : ' + str(type(threshold_value)))

  def setExtentValue(self, extent_value):
    if isinstance(extent_value, float) or isinstance(extent_value, int):
      self.extent_value = extent_value
    else:
      raise ValueError('Extent value must be "int" or "float" type, not : ' + str(type(extent_value)))

  def setMasking(self, masking):
    self.masking_container.setMasking(masking)

  def disableMasking(self):
    self.masking_container.disable()

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
      batch_list.extend(self.masking_container.getStringListForBatch())
      return batch_list
    else:
      raise ValueError('Unvalid contrast query, contrast index list not found')
