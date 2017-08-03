# -*- coding: utf-8 -*-
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
import numbers

class EstimationOptions():
  """
  Various  options  can  be  adjusted  in  order to improve the performance of the algorithm
  with your data.  Knowing what works best should be a matter of empirical exploration. For
  example,   if   your   data  has  very  little  intensity  nonuniformity  artifact,  then  the  bias
  regularisation  should  be  increased.  This  effectively  tells the algorithm that there is very
  little bias in your data, so it does not try to model it.
  """
  def __init__(self):
    self.tissue_probility_map_path = None
    self.ngaus = "[2 2 2 3 4 2]"
    self.bias_regularisation = "0.0001"
    self.bias_FWHM = "60"
    self.affine_regularisation = "mni"
    self.warping_regularisation = '4'
    self.sampling_distance = '3'
  
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setTissueProbilityMapPath(self, tissue_probility_map_path):
    self.tissue_probility_map_path = tissue_probility_map_path
     #===========================================================================   
  def setGaussianPerClassesList(self, gaussian_list):
    if len(gaussian_list) == 6:
      gauss_str_list = [str(gaussian) for gaussian in gaussian_list]
      self.ngaus = '[' + ' '.join(gauss_str_list) + ']'
    else:
      raise ValueError("gaussian list must contain 6 elements, not " + str(len(gaussian_list)))
    #===========================================================================  
  def unsetBiasRegularisation(self):
    self.bias_regularisation = '0'
    
  def setBiasRegularisationToExtremelyLight(self):
    self.bias_regularisation = '0.00001'
    
  def setBiasRegularisationToVeryLight(self):
    self.bias_regularisation = '0.0001'
    
  def setBiasRegularisationToLight(self):
    self.bias_regularisation = '0.001'
    
  def setBiasRegularisationToMedium(self):
    self.bias_regularisation = '0.01'
    
  def setBiasRegularisationToHeavy(self):
    self.bias_regularisation = '0.1'
    
  def setBiasRegularisationToVeryHeavy(self):
    self.bias_regularisation = '1'
    
  def setBiasRegularisationToExtremelyHeavy(self):
    self.bias_regularisation = '10'
    #===========================================================================    
  def unsetBiasFWHM(self):
    self.bias_FWHM = 'Inf'

  def setBiasFWHMTo30cutoff(self):
    self.bias_FWHM = '30'

  def setBiasFWHMTo40cutoff(self):
    self.bias_FWHM = '40'

  def setBiasFWHMTo50cutoff(self):
    self.bias_FWHM = '50'

  def setBiasFWHMTo60cutoff(self):
    self.bias_FWHM = '60'

  def setBiasFWHMTo70cutoff(self):
    self.bias_FWHM = '70'

  def setBiasFWHMTo80cutoff(self):
    self.bias_FWHM = '80'

  def setBiasFWHMTo90cutoff(self):
    self.bias_FWHM = '90'

  def setBiasFWHMTo100cutoff(self):
    self.bias_FWHM = '100'

  def setBiasFWHMTo110cutoff(self):
    self.bias_FWHM = '110'

  def setBiasFWHMTo120cutoff(self):
    self.bias_FWHM = '120'

  def setBiasFWHMTo130cutoff(self):
    self.bias_FWHM = '130'

  def setBiasFWHMTo140cutoff(self):
    self.bias_FWHM = '140'

  def setBiasFWHMTo150cutoff(self):
    self.bias_FWHM = '150'
    #===========================================================================    
  def setAffineRegularisationToEuropeanBrains(self):
    self.affine_regularisation = 'mni'
    
  def setAffineRegularisationToAsianBrains(self):
    self.affine_regularisation = 'eastern'
    
  def setAffineRegularisationToAverageSizedTemplate(self):
    self.affine_regularisation = 'subj'
    
  def unsetAffineRegularisation(self):
    self.affine_regularisation = ''
    
  def unsetRegularisation(self):
    self.affine_regularisation = 'none'
    #===========================================================================    
  @checkIfArgumentTypeIsAllowed(int, 1)
  def setWarpingRegularisation(self, regularisation_number):
    self.warping_regularisation = regularisation_number
    #===========================================================================     
  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
  def setSamplingDistance(self, sampling_distance):
    self.sampling_distance = sampling_distance
    
  def getStringListForBatch(self):
    if self.tissue_probility_map_path is not None:
      batch_list = []
      batch_list.append("opts.tpm = {'%s'};" % self.tissue_probility_map_path)
      batch_list.append("opts.ngaus = %s;" % self.ngaus)
      batch_list.append("opts.biasreg = %s;" % self.bias_regularisation)
      batch_list.append("opts.biasfwhm = %s;" % self.bias_FWHM)
      batch_list.append("opts.affreg = '%s';" % self.affine_regularisation)
      batch_list.append("opts.warpreg = %s;" % self.warping_regularisation)
      batch_list.append("opts.samp = %s;" % self.sampling_distance)
      return batch_list
    else:
      raise ValueError('TPM path is required')
    