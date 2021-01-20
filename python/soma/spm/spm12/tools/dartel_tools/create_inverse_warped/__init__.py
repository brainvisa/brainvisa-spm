# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.tools.dartel_tools.create_inverse_warped import CreateInverseWarped as CreateInverseWarped_virtual
from soma.spm.spm_main_module import SPM12MainModule

class CreateInverseWarped(CreateInverseWarped_virtual, SPM12MainModule):
  def __init__(self):
    self.flow_field_list = []
    self.image_path_list = []
    self.time_steps = 6
    self.interpolation = 1
    self.output_warped_path_list = None
    
    
