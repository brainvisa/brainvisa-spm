# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.stats.model_estimation import ModelEstimation
from soma.spm.virtual_spm.stats.model_estimation import ModelEstimationClassical as ModelEstimationClassical_virtual
from soma.spm.virtual_spm.stats.model_estimation import ModelEstimationBayesianSecondLevel as ModelEstimationBayesianSecondLevel_virtual
from soma.spm.virtual_spm.stats.model_estimation import ModelEstimationBayesianFirstLevel as ModelEstimationBayesianFirstLevel_virtual
from soma.spm.spm_main_module import SPM8MainModule

from soma.spm.spm8.stats.model_estimation.anova import ANOVA
from soma.spm.spm8.stats.model_estimation.simple_contrast_container import SimpleContrastContainer
from soma.spm.spm8.stats.model_estimation.analysis_space import AnalysisSpaceVolume


#==============================================================================
#
#==============================================================================
class ModelEstimationClassical(ModelEstimation, ModelEstimationClassical_virtual, SPM8MainModule):
  def __init__(self):
    ModelEstimation.__init__(self)
#==============================================================================
#
#==============================================================================
class ModelEstimationBayesianSecondLevel(ModelEstimation, ModelEstimationBayesianSecondLevel_virtual, SPM8MainModule):
  def __init__(self):
    ModelEstimation.__init__(self)
#==============================================================================
#
#==============================================================================
class ModelEstimationBayesianFirstLevel(ModelEstimation, ModelEstimationBayesianFirstLevel_virtual, SPM8MainModule):
  def __init__(self):
    ModelEstimation.__init__(self)
    self.analysis_space = AnalysisSpaceVolume()
    self.possible_signal_priors_list = ['UGL', 'GMRF', 'LORETA', 'WGL', 'Global', 'Uninformative']
    self.signal_priors = 'UGL'
    self.AR_model_order_vector = [3]
    self.possible_noise_priors_list = ['UGL', 'GMRF', 'LORETA', 'Tissue-type', 'Robust']
    self.noise_priors = 'UGL'
    self.tissue_type_path = None
    self.log_evidence_map = 'No'
    self.ANOVA = ANOVA()
    self.simple_contrast_container = SimpleContrastContainer()
