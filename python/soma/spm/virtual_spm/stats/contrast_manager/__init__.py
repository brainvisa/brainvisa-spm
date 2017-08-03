# -*- coding: utf-8 -*-
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsStrOrUnicode
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

class ContrastManager():
  """
  Set up T and F contrasts.
  """
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setMatlabFilePath(self, matlab_file_path):
    """
    Select SPM.mat file for contrasts
    """
    self.matlab_file_path = matlab_file_path

  def deleteExistingContrast(self):
    """
    Delete existing contrasts
    """
    self.delete_existing_contrast = 1

  def keepExistingContrast(self):
    self.delete_existing_contrast = 0
#==============================================================================
  def appendContrast(self, contrast):
    self.contrast_container.append(contrast)

  def clearContrastList(self):
    self.contrast_container.clear()
#==============================================================================
  
  def getStringListForBatch( self ):
    if self.matlab_file_path is not None:
      batch_list = []
      batch_list.append("spm.stats.con.spmmat = {'%s'};" % self.matlab_file_path)
      batch_list.append("spm.stats.con.delete = %i;" % self.delete_existing_contrast)
      batch_list.extend(addBatchKeyWordInEachItem("spm.stats.con", self.contrast_container.getStringListForBatch()))
      return batch_list
    else:
      raise ValueError('Unvalid Model estimation, Mat file not found')
  


