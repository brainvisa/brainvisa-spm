# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.stats.factorial_design.masking import Masking as Masking_virtual
from soma.spm.virtual_spm.stats.factorial_design.masking import ThresholdMasking as ThresholdMasking_virtual

class Masking(Masking_virtual):
  def __init__(self):
    self.threshold_masking = ThresholdMasking()
    self.implicit_mask = True
    self.explicit_mask_path = None

class ThresholdMasking(ThresholdMasking_virtual):
  def __init__(self):
    self.method = 'None'
    self.threshold = None
