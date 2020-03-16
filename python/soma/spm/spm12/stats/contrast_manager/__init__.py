# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm_main_module import SPM12MainModule
from soma.spm.virtual_spm.stats.contrast_manager import ContrastManager as ContrastManager_virtual
from soma.spm.spm12.stats.contrast_manager.contrast_container import ContrastContainer

class ContrastManager(ContrastManager_virtual, SPM12MainModule):
  def __init__(self):
    self.matlab_file_path = None
    self.contrast_container = ContrastContainer()
    self.delete_existing_contrast = False
