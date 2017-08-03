# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.tools.hdw import HDW as HDW_virtual
from soma.spm.spm8.tools.hdw.subject_container import SubjectContainer
from soma.spm.spm8.tools.hdw.bias_correction_options import BiasCorrectionOptions
from soma.spm.spm8.tools.hdw.warping_options import WarpingOptions

from soma.spm.spm_main_module import SPM8MainModule

class HDW(HDW_virtual, SPM8MainModule):
  def __init__(self):
    self.subject_container = SubjectContainer()
    self.bias_correction_options = BiasCorrectionOptions()
    self.warping_options = WarpingOptions()