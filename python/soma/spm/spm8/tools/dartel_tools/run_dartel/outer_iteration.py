# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.tools.dartel_tools.run_dartel.outer_iteration import OuterIteration as OuterIteration_virtual

class OuterIteration(OuterIteration_virtual):
  def __init__(self):
    self.inner_iterations = 3
    self.reg_params = [0.1, 0.01, 0.001]
    self.time_steps = 6
    self.smoothing_parameter = 1
    