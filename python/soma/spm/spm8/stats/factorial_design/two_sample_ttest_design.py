# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.stats.factorial_design.two_sample_ttest_design import TwoSampleTTestDesign as TwoSampleTTestDesign_virtual

class TwoSampleTTestDesign(TwoSampleTTestDesign_virtual):
  def __init__(self):
    self.group_1_scans = None
    self.group_2_scans = None
    self.independence = 0
    self.variance = 1
    self.grand_mean_scaling = 0
    self.ANCOVA = 0
