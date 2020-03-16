# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem, convertPathListToSPMBatchString

from soma.spm.virtual_spm.stats.model_estimation.analysis_space import AnalysisSpace

class ModelEstimation(object):
  """
  Model  parameters  can be estimated using classical (ReML - Restricted Maximum
  Likelihood)  or  Bayesian  algorithms.  After  parameter  estimation,  the  RESULTS
  button  can  be  used  to specify contrasts that will produce Statistical Parametric
  Maps (SPMs) or Posterior Probability Maps (PPMs) and tables of statistics.
  """
  def __init__(self):
    self.matlab_file_path = None

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setMatlabFilePath(self, matlab_file_path):
    """
    Select the SPM.mat file that contains the design specification. 
    The directory containing this file is known as the input directory.
    """
    self.matlab_file_path = matlab_file_path
#==============================================================================
#
#==============================================================================
class ModelEstimationClassical(ModelEstimation):  
  """
  Model  parameters  are  estimated  using  Restricted Maximum Likelihood (ReML).
  This  assumes  the  error  correlation  structure  is  the  same  at each voxel. This
  correlation   can   be   specified  using  either  an  AR(1)  or  an  Independent  and
  Identically  Distributed  (IID)  error  model. These options are chosen at the model
  specification  stage.  ReML  estimation  should  be  applied  to spatially smoothed
  functional images.
  After   estimation,   specific   profiles  of  parameters  are  tested  using  a  linear
  compound  or  contrast  with  the  T  or  F  statistic. The resulting statistical map
  constitutes  an  SPM.  The  SPM{T}/{F}  is  then  characterised  in terms of focal or
  regional differences by assuming that (under the null hypothesis) the components
  of the SPM (ie. residual fields) behave as smooth stationary Gaussian fields.
  """
  def getStringListForBatch( self ):
    if self.matlab_file_path is not None:
      batch_list = ["spm.stats.fmri_est.spmmat = {'%s'};" % self.matlab_file_path]
      batch_list.append("spm.stats.fmri_est.method.Classical = 1;")
      return batch_list
    else:
      raise ValueError('Unvalid Model estimation, Mat file not found')
#==============================================================================
#
#==============================================================================
class ModelEstimationBayesianSecondLevel(ModelEstimation):
  """
  Bayesian  estimation  of  2nd  level  models.  This option uses the Empirical Bayes
  algorithm  with global shrinkage priors that was previously implemented in SPM2.
  Use  of the global shrinkage prior embodies a prior belief that, on average over all
  voxels,  there  is  no net experimental effect. Some voxels will respond negatively
  and some positively with a variability determined by the prior precision. This prior
  precision can be estimated from the data using Empirical Bayes.
  This item has a constant value which can not be modified using the GUI.
  """
  def getStringListForBatch( self ):
    if self.matlab_file_path is not None:
      batch_list = ["spm.stats.fmri_est.spmmat = {'%s'};" % self.matlab_file_path]
      batch_list.append("spm.stats.fmri_est.method.Bayesian2 = 1;")
      return batch_list
    else:
      raise ValueError('Unvalid Model estimation, Mat file not found')
#==============================================================================
#
#==============================================================================
class ModelEstimationBayesianFirstLevel(ModelEstimation):
  """
  There  are  three  possible  estimation  procedures  for  fMRI  models (1) classical
  (ReML)  estimation of first or second level models, (2) Bayesian estimation of first
  level  models  and (3) Bayesian estimation of second level models. Option (2) uses
  a  Variational  Bayes  (VB)  algorithm  that  is  new  to  SPM5.  Option (3) uses the
  Empirical Bayes algorithm with global shrinkage priors that was also in SPM2.
  To  use  option  (3)  you  must have already estimated the model using option (1).
  That  is, for second-level models you must run a ReML estimation before running
  a Bayesian estimation. This is not necessary for option (2). Bayesian estimation of
  1st-level models using VB does not require a prior ReML estimation.
  """
#==============================================================================
  @checkIfArgumentTypeIsAllowed(AnalysisSpace, 1)
  def setAnalysisSpace(self, analysis_space):
    del self.analysis_space
    self.analysis_space = analysis_space
#==============================================================================
  def setSignalPriorsToUGL(self):
    self.signal_priors = "UGL"
    
  def setSignalPriorsToGRMF(self):
    self.signal_priors = "GRMF"
    
  def setSignalPriorsToLORETA(self):
    self.signal_priors = "LORETA"
    
  def setSignalPriorsToWGL(self):
    self.signal_priors = "WGL"
    
  def setSignalPriorsToGlobal(self):
    self.signal_priors = "Global"
    
  def setSignalPriorsToUninformative(self):
    self.signal_priors = "Uninformative"
#==============================================================================    
  @checkIfArgumentTypeIsAllowed(int, 1)
  def setARModelOrder(self, AR_model_order):
    self.AR_model_order_vector = [AR_model_order]

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setARModelOrderVector(self, AR_model_order_vector):
    self.AR_model_order_vector = AR_model_order_vector
#==============================================================================  
  def setNoisePriorsToUGL(self):
    self.noise_priors = "UGL"
    self.tissue_type_list = None
    
  def setNoisePriorsToGMRF(self):
    self.noise_priors = "GMRF"
    self.tissue_type_list = None
    
  def setNoisePriorsToLORETA(self):
    self.noise_priors = "LORETA"
    self.tissue_type_list = None
    
  def setNoisePriorsToTissueType(self):
    self.noise_priors = "Tissue-type"
    self.tissue_type_list = []
    
  def setNoisePriorsToRobust(self):
    self.noise_priors = "Robust"
    self.tissue_type_list = None
#==============================================================================  
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def appendTissueType(self, tissue_type_path):
    self.tissue_type_list.append(tissue_type_path)

  def saveLogEvidenceMap(self):
    self.log_evidence_map = 'Yes'

  def discardLogEvidenceMap(self):
    self.log_evidence_map = 'No'
#==============================================================================
  def enableFirstLevelANOVA(self):
    self.ANOVA.enableFirstLevel()

  def disableFirstLevelANOVA(self):
    self.ANOVA.disableFirstLevel()

  def enableSecondLevelANOVA(self):
    self.ANOVA.enableSecondLevel()

  def disableSecondLevelANOVA(self):
    self.ANOVA.disableSecondLevel()
#==============================================================================
  def appendSimpleContrast(self, simple_contrast):
    self.simple_contrast_container.append(simple_contrast)

  def clearSimpleContrastList(self):
    self.simple_contrast_container.clear()
#==============================================================================  
  def getStringListForBatch( self ):
    if self.matlab_file_path is not None:
      batch_list = ["spm.stats.fmri_est.spmmat = {'%s'};" % self.matlab_file_path]
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

