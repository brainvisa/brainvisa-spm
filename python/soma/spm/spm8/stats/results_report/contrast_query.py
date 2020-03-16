# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.stats.results_report.contrast_query import ContrastQuery as ContrastQuery_virtual

from soma.spm.spm8.stats.results_report.masking_container import MaskingContainer

class ContrastQuery(ContrastQuery_virtual):
  def __init__(self):
    self.title = ''
    self.contrast_index_list = None
    self.threshold_type = 'FWE'
    self.threshold_value = 0.05
    self.extent_value = 0
    self.masking_container = MaskingContainer()
