# -*- coding: utf-8 -*-
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsStrOrUnicode
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

class ResultsReport():
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setMatlabFilePath(self, matlab_file_path):
    """
    Select the SPM.mat file that contains the design specification.
    """
    self.matlab_file_path = matlab_file_path

  def appendContrastQuery(self, contrast_query):
    self.contrast_query_container.append(contrast_query)

  def clearContrastQueryList(self):
    self.contrast_query_container.clear()

  def setDataTypeToVolumetric(self):
    """
    Data  type.  This  option  is  only  meaningful  for  M/EEG  data.  Keep the default
    'Volumetric' for any other kind of data.
    """
    self.data_type = 1

  def setDataTypeToScalpTime(self):
    """
    Data  type.  This  option  is  only  meaningful  for  M/EEG  data.  Keep the default
    'Volumetric' for any other kind of data.
    """
    self.data_type = 2

  def setDataTypeToScalpFrequency(self):
    """
    Data  type.  This  option  is  only  meaningful  for  M/EEG  data.  Keep the default
    'Volumetric' for any other kind of data.
    """
    self.data_type = 3

  def setDataTypeToTimeFrequency(self):
    """
    Data  type.  This  option  is  only  meaningful  for  M/EEG  data.  Keep the default
    'Volumetric' for any other kind of data.
    """
    self.data_type = 4

  def setDataTypeToFrequencyFrequency(self):
    """
    Data  type.  This  option  is  only  meaningful  for  M/EEG  data.  Keep the default
    'Volumetric' for any other kind of data.
    """
    self.data_type = 5

  def enablePrintResult(self):
    self.print_result = 'true'

  def disablePrintResult(self):
    self.print_result = 'false'

  def getStringListForBatch( self ):
    if self.matlab_file_path is not None:
      batch_list = []
      batch_list.append("spm.stats.results.spmmat = {'%s'};" % self.matlab_file_path)
      batch_list.append("spm.stats.results.units = %i;" % self.data_type)
      batch_list.append("spm.stats.results.print = %s;" % self.print_result)
      batch_list.extend(addBatchKeyWordInEachItem("spm.stats.results", self.contrast_query_container.getStringListForBatch()))
      return batch_list
    else:
      raise ValueError('Unvalid Model estimation, Mat file not found')
