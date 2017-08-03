# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.util.image_calculator.options import Options as Options_virtual

class Options(Options_virtual):
  def __init__(self):
    self.data_matrix = 0
    self.masking_type = 0
    self.interpolation = 1
    self.data_type = 4