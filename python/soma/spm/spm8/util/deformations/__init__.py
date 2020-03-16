# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.virtual_spm.util.deformations import Deformations as Deformations_virtual
from soma.spm.spm8.util.deformations.composition import Composition
from soma.spm.spm8.util.deformations.composition import Deformation
from soma.spm.spm_main_module import SPM8MainModule

class Deformations(Deformations_virtual, SPM8MainModule):
  def __init__(self):
    self.composition = Composition()
    self.composition_name = ''
    self.image_path_list = ''
    self.output_destination = "current directory"
    self.output_destination_path = None
    self.interpolation = 1
    
    self.composition_path = None
    self.deformed_image_path_list = None
    
  @checkIfArgumentTypeIsAllowed(Deformation, 1)
  def appendDeformation(self, deformation):
    self.composition.append(deformation)
  