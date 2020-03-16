# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.spatial.normalise.writing_options import WritingOptions as WritingOptions_virtual
import numpy

class WritingOptions(WritingOptions_virtual):
  def __init__(self):
    self.preserve = 0
    self.bounding_box = numpy.array([[-78, -112, -70],[78, 76, 85]])
    self.voxel_size = [2, 2, 2]
    self.interpolation = 1
    self.wrapping = [0, 0, 0]
    self.filename_prefix = 'w'
