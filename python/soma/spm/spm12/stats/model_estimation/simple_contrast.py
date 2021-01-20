# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.stats.model_estimation.simple_contrast import SimpleContrast as SimpleContrast_virtual

class SimpleContrast(SimpleContrast_virtual):
  def __init__(self):
    self.name = None
    self.vector = None
