 # -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.spatial.coregister import EstimateAndReslice as EstimateAndReslice_virtual
from soma.spm.virtual_spm.spatial.coregister import Estimate as Estimate_virtual
from soma.spm.spm8.spatial.coregister.estimation_options import EstimationOptions
from soma.spm.spm8.spatial.coregister.reslice_options import ResliceOptions

from soma.spm.spm_main_module import SPM8MainModule

class EstimateAndReslice(EstimateAndReslice_virtual, SPM8MainModule):
  def __init__(self):
    self.reference_volume_path = None
    self.source_volume_path = None
    self.other_volume_path_list = None
    self.estimation_options = EstimationOptions()
    self.reslice_options = ResliceOptions()
    
    self.source_warped_volume_path = None
    self.other_warped_volume_path_list = None
#===============================================================================
# 
#===============================================================================
class Estimate(Estimate_virtual, SPM8MainModule):
  def __init__(self):
    self.reference_volume_path = None
    self.source_volume_path = None
    self.other_volume_path_list = None
    self.estimation_options = EstimationOptions()