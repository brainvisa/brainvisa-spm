# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.spatial.realign.reslice_options import ResliceOptions as ResliceOptions_virtual


class ResliceOptions(ResliceOptions_virtual):
  def __init__(self):
    self.resliced_images = [2, 1]
    self.interpolation = '4'
    self.wrapping = [0, 0, 0]
    self.masking = 1
    self.filename_prefix = 'r'
    