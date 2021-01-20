 # -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.tools.hdw.warping_options import WarpingOptions as WarpingOptions_virtual

class WarpingOptions(WarpingOptions_virtual):
  def __init__(self):
    self.iteration = 8
    self.warping_regularisation = 4