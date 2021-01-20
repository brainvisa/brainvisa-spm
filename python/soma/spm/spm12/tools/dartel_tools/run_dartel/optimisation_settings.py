# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.tools.dartel_tools.run_dartel.optimisation_settings import OptimisationSettings as OptimisationSettings_virtual

class OptimisationSettings(OptimisationSettings_virtual):
  def __init__(self):
    self.LM_regularisation = 0.01
    self.cycles = 3
    self.iterations = 3
    