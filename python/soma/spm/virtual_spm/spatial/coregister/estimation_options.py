# -*- coding: utf-8 -*-
from soma.spm.spm_batch_maker_utils import convertlistToSPMString
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed

class EstimationOptions():
  """
  Various registration options, which are passed to the Powell optimisation algorithm.
  """
    #===========================================================================    
  def setObjectiveFunctionToMutualInformation(self):
    """
    Registration  involves  finding parameters that either maximise or minimise some objective
    function.   For   inter-modal   registration,   use   Mutual   Information,  Normalised  Mutual
    Information,  or  Entropy  Correlation  Coefficient.
    """
    self.objective_function = 'mi'
     
  def setObjectiveFunctionToNormalisedMutualInformation(self):
    """
    Registration  involves  finding parameters that either maximise or minimise some objective
    function.   For   inter-modal   registration,   use   Mutual   Information,  Normalised  Mutual
    Information,  or  Entropy  Correlation  Coefficient.
    """
    self.objective_function = 'nmi'
     
  def setObjectiveFunctionToEntropyCorrelationCoefficient(self):
    """
    Registration  involves  finding parameters that either maximise or minimise some objective
    function.   For   inter-modal   registration,   use   Mutual   Information,  Normalised  Mutual
    Information,  or  Entropy  Correlation  Coefficient.
    """
    self.objective_function = 'ecc'
     
  def setObjectiveFunctionToNormalisedCrossCorrelation(self):
    """
    Registration  involves  finding parameters that either maximise or minimise some objective
    function. For  within  modality,  you could also use Normalised Cross Correlation.
    """
    self.objective_function = 'ncc'
    #===========================================================================    
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setSeparation(self, separation_list):
    """
    The  average distance between sampled points (in mm).  Can be a vector to allow a coarse
    registration followed by increasingly fine ones.
    """
    self.separation = separation_list
    
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setTolerances(self, tolerance_list):
    """
    The  accuracy  for  each parameter.  Iterations stop when differences between successive
    estimates are less than the required tolerance.
    
    """
    if len(tolerance_list) == 12:
      self.tolerances = tolerance_list
    else:
      raise ValueError("Tolerances list must contains 12 elements")
    
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setHistogramSmoothing(self, histogram_smoothing_list):
    """
    Gaussian  smoothing to apply to the 256x256 joint histogram. Other information theoretic
    coregistration  methods  use  fewer  bins,  but  Gaussian  smoothing  seems  to  be  more
    elegant.
    """
    if len(histogram_smoothing_list) == 2:
      self.histogram_smoothing = histogram_smoothing_list
    else:
      raise ValueError("Tolerances list must contains 2 elements")
      

  def getStringListForBatch(self):
    batch_list = []
    batch_list.append("eoptions.cost_fun = '%s';" % self.objective_function)
    batch_list.append("eoptions.sep = %s;" % convertlistToSPMString(self.separation))
    batch_list.append("eoptions.tol = %s;" % convertlistToSPMString(self.tolerances))
    batch_list.append("eoptions.fwhm = %s;" % convertlistToSPMString(self.histogram_smoothing))
    return batch_list
    