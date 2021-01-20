 # -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.tools.hdw.bias_correction_options import BiasCorrectionOptions as BiasCorrectionOptions_virtual

class BiasCorrectionOptions(BiasCorrectionOptions_virtual):
  def __init__(self):
    self.iteration = 8
    self.bias_fwhm = 60
    self.bias_regularisation = 1e-06
    self.LM_regularisation = 1e-06
    