# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.spatial.realign import EstimateAndReslice as EstimateAndReslice_virtual
from soma.spm.spm12.spatial.realign.estimation_options import EstimationOptions
from soma.spm.spm12.spatial.realign.reslice_options import ResliceOptions

from soma.spm.spm_main_module import SPM12MainModule


class EstimateAndReslice(EstimateAndReslice_virtual, SPM12MainModule):
  def __init__(self):
    self.session_path_list = []
    self.session_realigned_path_list = []
    self.mean_output_path = None
    self.realignment_parameters_path_list = []

    self.estimation_options = EstimationOptions()
    self.reslice_options = ResliceOptions()
