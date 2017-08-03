# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.spatial.coregister.estimation_options import EstimationOptions as EstimationOptions_virtual

class EstimationOptions(EstimationOptions_virtual):
  def __init__(self):
    self.objective_function = "nmi"
    self.separation = [4, 2]
    self.tolerances = [0.02, 0.02, 0.02, 0.001, 0.001, 0.001, 0.01, 0.01, 0.01, 0.001, 0.001, 0.001]
    self.histogram_smoothing = [7, 7]
