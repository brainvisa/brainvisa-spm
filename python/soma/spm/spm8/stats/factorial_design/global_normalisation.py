# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.stats.factorial_design.global_normalisation import GlobalNormalisation as GlobalNormalisation_virtual
from soma.spm.virtual_spm.stats.factorial_design.global_normalisation import OverallGrandMeanScaling as OverallGrandMeanScaling_virtual

class GlobalNormalisation(GlobalNormalisation_virtual):
  def __init__(self):
    self.overall_grand_mean_scaling = OverallGrandMeanScaling()
    self.normalisation = 1


class OverallGrandMeanScaling(OverallGrandMeanScaling_virtual):
  def __init__(self):
    self.is_activate = False
    self.grand_mean_scaled_value = []
    
