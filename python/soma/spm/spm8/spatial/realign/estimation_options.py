# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.spatial.realign.estimation_options import EstimationOptions as EstimationOptions_virtual


class EstimationOptions(EstimationOptions_virtual):
  def __init__(self):
    self.quality = 0.9
    self.separation = 4
    self.fwhm = 5
    self.num_passes = 1
    self.interpolation = 2
    self.wrapping = [0, 0, 0]
    self.weighting_image_path = ''