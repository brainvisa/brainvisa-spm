# -*- coding: utf-8 -*-
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
from soma.spm.virtual_spm.util.deformations import Deformations as Deformations_virtual
from soma.spm.spm12.util.deformations.composition import Composition
from soma.spm.spm12.util.deformations.composition import Deformation
from soma.spm.spm12.util.deformations.output_container import OutputContainer
from soma.spm.spm12.util.deformations.output import Output
from soma.spm.spm_main_module import SPM12MainModule

class Deformations(Deformations_virtual, SPM12MainModule):
  def __init__(self):
    self.composition = Composition()
    self.output_container = OutputContainer()
    
    self.composition_path = None
    self.deformed_image_path_list = None
    
  @checkIfArgumentTypeIsAllowed(Deformation, 1)
  def appendDeformation(self, deformation):
    self.composition.append(deformation)
    
  @checkIfArgumentTypeIsAllowed(Output, 1)
  def appendOutput(self, output):
    self.output_container.append(output)
    
  def getStringListForBatch( self ):
    if self.composition:      
      batch_list = []
      batch_list.extend(addBatchKeyWordInEachItem("spm.util.defs", self.composition.getStringListForBatch()))
      batch_list.extend(addBatchKeyWordInEachItem("spm.util.defs", self.output_container.getStringListForBatch()))
      return batch_list
    else:
      raise ValueError("At least one composition is required")
    
  def _moveSPMDefaultPathsIfNeeded(self):
    self.output_container._moveSPMDefaultPathsIfNeeded()