# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.tools.dartel_tools.create_warped import CreateWarped as CreateWarped_virtual
from soma.spm.spm_main_module import SPM12MainModule

class CreateWarped(CreateWarped_virtual, SPM12MainModule):
  def __init__(self):
    self.flow_field_list = []
    self.images_list_list = []
    self.modulation = 0
    self.time_steps = 6
    self.interpolation = 1
    self.output_warped_path_list_list = None
    
    self._unmodulated_prefix = 'w'
    self._modulated_prefix = 'mw'
    
