# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.stats.results_report.masking import Masking as Masking_virtual

class Masking(Masking_virtual):
  def __init__(self):
    self.contrast_index_list = None
    self.mask_threshold_value = 0.05
    self.mask_nature = None
