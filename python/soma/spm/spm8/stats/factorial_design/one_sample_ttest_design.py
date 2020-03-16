# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.stats.factorial_design.one_sample_ttest_design import OneSampleTTestDesign as OneSampleTTestDesign_virtual

class OneSampleTTestDesign(OneSampleTTestDesign_virtual):
  def __init__(self):
    self.scans = None
