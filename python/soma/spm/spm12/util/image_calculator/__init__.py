# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.util.image_calculator import ImageCalculator as ImageCalculator_virtual
from soma.spm.spm12.util.image_calculator.options import Options
from soma.spm.spm12.util.image_calculator.additional_variable_container import AdditionalVariableContainer
from soma.spm.spm_main_module import SPM12MainModule
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

class ImageCalculator(ImageCalculator_virtual, SPM12MainModule):
  def __init__(self):
    self.input_path_list = None
    self.output_path = 'output.img'
    self.output_directory = ''
    self.expression = None
    self.options = Options()
    self.additional_variable_container = AdditionalVariableContainer()
    
  def appendAdditionalVariable(self, additional_variable):
    self.additional_variable_container.append(additional_variable)
    
  def getStringListForBatch( self ):
    if not None in [self.input_path_list, self.expression]:
      batch_list = []
      image_path_list_for_batch = []
      for image_path in self.input_path_list:
        image_path_list_for_batch.append("'%s,1'" % image_path)
      image_path_for_batch = '\n'.join(image_path_list_for_batch)
      
      batch_list.append("spm.util.imcalc.input = {%s};" %image_path_for_batch)
      batch_list.append("spm.util.imcalc.output = '%s';" %self.output_path)
      batch_list.append("spm.util.imcalc.outdir = {'%s'};" %self.output_directory)
      batch_list.append("spm.util.imcalc.expression = '%s';" %self.expression)
      batch_list.extend(addBatchKeyWordInEachItem("spm.util.imcalc", self.additional_variable_container.getStringListForBatch()))
      batch_list.extend(addBatchKeyWordInEachItem("spm.util.imcalc", self.options.getStringListForBatch()))
      return batch_list
    else:
      raise ValueError("Missing input_path_list and/or expression")