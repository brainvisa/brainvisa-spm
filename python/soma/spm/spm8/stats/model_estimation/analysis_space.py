# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.stats.model_estimation.analysis_space import AnalysisSpace as AnalysisSpace_virtual
from soma.spm.virtual_spm.stats.model_estimation.analysis_space import AnalysisSpaceVolume as AnalysisSpaceVolume_virtual
from soma.spm.virtual_spm.stats.model_estimation.analysis_space import AnalysisSpaceSlices as AnalysisSpaceSlices_virtual
from soma.spm.virtual_spm.stats.model_estimation.analysis_space import AnalysisSpaceClusters as AnalysisSpaceClusters_virtual

class AnalysisSpace(AnalysisSpace_virtual):
  def __init__(self):
    self.block_type = 'Slices'
#==============================================================================    
class AnalysisSpaceVolume(AnalysisSpace, AnalysisSpaceVolume_virtual):
  def __init__(self):
    AnalysisSpace.__init__(self)
#==============================================================================
class AnalysisSpaceSlices(AnalysisSpace, AnalysisSpaceSlices_virtual):
  def __init__(self):
    AnalysisSpace.__init__(self)
    self.slice_number_list = None
#==============================================================================
class AnalysisSpaceClusters(AnalysisSpace, AnalysisSpaceClusters_virtual):
  def __init__(self):
    AnalysisSpace.__init__(self)
    self.cluster_mask_path = ''
#==============================================================================
