# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.spatial.smooth import Smooth as Smooth_virtual
from soma.spm.spm_main_module import SPM8MainModule
from soma.spm.spm_batch_maker_utils import convertlistToSPMString

class Smooth(Smooth_virtual, SPM8MainModule):
  def __init__(self):
    self.input_path_list = None
    self.output_path_list = None
    self.fwhm = convertlistToSPMString([8, 8, 8])
    self.data_type = 0
    self.implicit_masking = 0
    self.filename_prefix = 's'