# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.spatial.new_segment.channel import Channel as Channel_virtual

class Channel(Channel_virtual):
  def __init__(self):
    self.volume_path_list = []
    self.bias_regularisation = 0.0001
    self.bias_FWHM = '60'
    self.save_bias_corrected = [0, 0]

    self.bias_corrected_prefix = 'm'
    self.bias_field_prefix = 'BiasField_'

    self.bias_corrected_path_list = []
    self.bias_field_path_list = []


