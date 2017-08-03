# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.util.image_calculator import ImageCalculator as ImageCalculator_virtual
from soma.spm.spm8.util.image_calculator.options import Options
from soma.spm.spm_main_module import SPM8MainModule

class ImageCalculator(ImageCalculator_virtual, SPM8MainModule):
  def __init__(self):
    self.input_path_list = None
    self.output_path = 'output.img'
    self.output_directory = ''
    self.expression = None
    self.options = Options()