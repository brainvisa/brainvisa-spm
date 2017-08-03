# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.spatial.normalise.estimation_options import EstimationOptions as EstimationOptions_virtual

class EstimationOptions(EstimationOptions_virtual):
  def __init__(self):
    self.template_path = None
    self.template_weighting_path = ''
    self.source_image_smoothing = 8
    self.template_image_smoothing = 0
    self.affine_regularisation = 'mni'
    self.cutoff = 25
    self.iterations = 16
    self.affine_regularisation = 1 