# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.stats.factorial_design.global_calculation import GlobalCalculation as GlobalCalculation_virtual

class GlobalCalculation(GlobalCalculation_virtual):
  def __init__(self):
    self.possible_method_list = ['Omit', 'User', 'Mean']
    self.method = 'Omit'
    self.user_global_values_list = []
