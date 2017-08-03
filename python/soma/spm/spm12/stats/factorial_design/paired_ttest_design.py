# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.stats.factorial_design.paired_ttest_design import PairedTTestDesign as PairedTTestDesign_virtual
from soma.spm.virtual_spm.stats.factorial_design.paired_ttest_design import ScansPair as ScansPair_virtual

class PairedTTestDesign(PairedTTestDesign_virtual):
  def __init__(self):
    self.scans_pair_list = []
    self.grand_mean_scaling = 0
    self.ANCOVA = 0
    
class ScansPair(ScansPair_virtual):
  def __init__(self):
    self.scan_1 = None
    self.scan_2 = None
