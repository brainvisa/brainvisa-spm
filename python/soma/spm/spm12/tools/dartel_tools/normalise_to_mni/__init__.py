# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.tools.dartel_tools.normalise_to_mni import NormaliseToMNI as NormaliseToMNI_virtual
from soma.spm.spm_main_module import SPM12MainModule
from soma.spm.spm_batch_maker_utils import convertlistToSPMString
import numpy

class NormaliseToMNI(NormaliseToMNI_virtual, SPM12MainModule):
  def __init__(self):
    self.final_template_path = ''
    self.according_to = None
    self.voxel_size = ["NaN", "NaN", "NaN"]
    self.bounding_box = numpy.array([["NaN", "NaN", "NaN"],["NaN", "NaN", "NaN"]])
    self.preserve = 0
    self.fwhm = convertlistToSPMString([8, 8, 8])

