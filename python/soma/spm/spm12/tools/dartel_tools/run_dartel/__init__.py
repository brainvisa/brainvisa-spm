# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.tools.dartel_tools.run_dartel import RunDartel as RunDartel_virtual
from soma.spm.spm12.tools.dartel_tools.run_dartel.settings import Settings
from soma.spm.spm_main_module import SPM12MainModule

class RunDartel(RunDartel_virtual, SPM12MainModule):
  def __init__(self):
    self.images_list_list = []
    self.settings = Settings()
    self.output_template_path_list = None
    self.output_flow_field_path_list = None
    self.flow_field_prefix = "u_"
    self.flow_field_suffix = '_' + self.settings.getTemplateBasename()
    
