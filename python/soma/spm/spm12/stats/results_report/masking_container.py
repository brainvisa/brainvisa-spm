# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.stats.results_report.masking_container import MaskingContainer as MaskingContainer_virtual

class MaskingContainer(MaskingContainer_virtual):
  def __init__(self):
    raise NotImplementedError("it is deprecated in SPM12")
