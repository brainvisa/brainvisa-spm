# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.spatial.coregister.reslice_options import ResliceOptions as ResliceOptions_virtual

class ResliceOptions(ResliceOptions_virtual):
  def __init__(self):
    self.interpolation = 4
    self.wrapping = [0, 0, 0]
    self.masking = 0
    self.filename_prefix = 'r'
      