# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.stats.model_estimation import ModelEstimation as ModelEstimation_virtual
from soma.spm.virtual_spm.stats.model_estimation import ModelEstimationClassical as ModelEstimationClassical_virtual
from soma.spm.virtual_spm.stats.model_estimation import ModelEstimationBayesianSecondLevel as ModelEstimationBayesianSecondLevel_virtual
from soma.spm.virtual_spm.stats.model_estimation import ModelEstimationBayesianFirstLevel as ModelEstimationBayesianFirstLevel_virtual
from soma.spm.spm_main_module import SPM12MainModule

from soma.spm.spm12.stats.model_estimation.anova import ANOVA
from soma.spm.spm12.stats.model_estimation.simple_contrast_container import SimpleContrastContainer
from soma.spm.spm12.stats.model_estimation.analysis_space import AnalysisSpaceVolume

from soma.spm.spm_batch_maker_utils import convertPathListToSPMBatchString, addBatchKeyWordInEachItem

#==============================================================================
#
#==============================================================================
class ModelEstimation(ModelEstimation_virtual):
  def __init__(self):
    self.matlab_file_path = None
    self.write_residuals = True

  def setWriteResiduals(self):
    """Write images of residuals to disk. This is only implemented for classical inference."""
    self.write_residuals = True

  def unsetWriteResiduals(self):
    """Write images of residuals to disk. This is only implemented for classical inference."""
    self.write_residuals = False

class ModelEstimationClassical(ModelEstimation, ModelEstimationClassical_virtual, SPM12MainModule):
  def __init__(self):
    ModelEstimation.__init__(self)

  def getStringListForBatch( self ):
    if self.matlab_file_path is not None:
      batch_list = ["spm.stats.fmri_est.spmmat = {'%s'};" % self.matlab_file_path]
      batch_list.append("spm.stats.fmri_est.write_residuals = %i;" % self.write_residuals)
      batch_list.append("spm.stats.fmri_est.method.Classical = 1;")
      return batch_list
    else:
      raise ValueError('Unvalid Model estimation, Mat file not found')
#==============================================================================
#
#==============================================================================
class ModelEstimationBayesianSecondLevel(ModelEstimation, ModelEstimationBayesianSecondLevel_virtual, SPM12MainModule):
  def __init__(self):
    ModelEstimation.__init__(self)

  def getStringListForBatch( self ):
    if self.matlab_file_path is not None:
      batch_list = ["spm.stats.fmri_est.spmmat = {'%s'};" % self.matlab_file_path]
      batch_list.append("spm.stats.fmri_est.write_residuals = %i;" % self.write_residuals)
      batch_list.append("spm.stats.fmri_est.method.Bayesian2 = 1;")
      return batch_list
    else:
      raise ValueError('Unvalid Model estimation, Mat file not found')
#==============================================================================
#
#==============================================================================
class ModelEstimationBayesianFirstLevel(ModelEstimation, ModelEstimationBayesianFirstLevel_virtual, SPM12MainModule):
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

  def getStringListForBatch( self ):
    if self.matlab_file_path is not None:
      batch_list = ["spm.stats.fmri_est.spmmat = {'%s'};" % self.matlab_file_path]
      batch_list.append("spm.stats.fmri_est.write_residuals = %i;" % self.write_residuals)
      batch_list.append("spm.stats.fmri_est.method.Bayesian.signal = '%s';" % self.signal_priors)
      if len(self.AR_model_order_vector) == 1:
        AR_model_order_str = str(self.AR_model_order_vector[0])
      else:
        coeff_order_str_list = [str(coeff) for coeff in self.AR_model_order_vector]
        AR_model_order_str = '[' + '\n'.join(coeff_order_str_list) + ']'
      batch_list.append("spm.stats.fmri_est.method.Bayesian.ARP = %s;" % AR_model_order_str)
      if self.noise_priors == "UGL":
        batch_list.append("spm.stats.fmri_est.method.Bayesian.UGL = 1;")
      elif self.noise_priors == "GMRF":
        batch_list.append("spm.stats.fmri_est.method.Bayesian.GMRF = 1;")
      elif self.noise_priors == "LORETA":
        batch_list.append("spm.stats.fmri_est.method.Bayesian.LORETA = 1;")
      elif self.noise_priors == "Tissue-type":
        if (self.tissue_type_list) == 1:
          batch_list.append("spm.stats.fmri_est.method.Bayesian.noise.tissue_type = '%s';" % self.tissue_type_list[0])
        elif (self.tissue_type_list) > 1:
          batch_list.append("spm.stats.fmri_est.method.Bayesian.noise.tissue_type = {%s};" % convertPathListToSPMBatchString(self.tissue_type_list))
        else:
          raise ValueError("At least one  tissue_type is required")
      elif self.noise_priors == "Robust":
        batch_list.append("spm.stats.fmri_est.method.Bayesian.Robust = 1;")
      else:
        raise ValueError("Unvalid noise_priors")

      batch_list.append("spm.stats.fmri_est.method.Bayesian.noise.%s = 1;" % self.noise_priors)
      batch_list.append("spm.stats.fmri_est.method.Bayesian.LogEv = '%s';" % self.log_evidence_map)
      batch_list.extend(addBatchKeyWordInEachItem("spm.stats.fmri_est.method.Bayesian", self.analysis_space.getStringListForBatch()))
      batch_list.extend(addBatchKeyWordInEachItem("spm.stats.fmri_est.method.Bayesian", self.ANOVA.getStringListForBatch()))
      batch_list.extend(addBatchKeyWordInEachItem("spm.stats.fmri_est.method.Bayesian", self.simple_contrast_container.getStringListForBatch()))
      return batch_list
    else:
      raise ValueError('Unvalid Model estimation, Mat file not found')
