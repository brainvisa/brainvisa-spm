# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.stats.model_estimation.anova import ANOVA as ANOVA_virtual

class ANOVA(ANOVA_virtual):
  def __init__(self):
    self.first_level = 'No'
    self.second_level = 'Yes'
