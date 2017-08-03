# -*- coding: utf-8 -*-
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
import numbers

class ExtendedOptions():
  def __init__(self):
    self.spatial_normalization = DartelSpatialNormalization()
    self.SANLM_denoising_filter = 2
    self.mrf_weighting = 0.15
    self.cleanup = 1
    self.print_result = 1
    
  def setDartelSpatialNormalization(self):
    del self.spatial_normalization
    self.spatial_normalization = DartelSpatialNormalization()
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setDartelTemplatePath(self, dartel_template_path):
    if isinstance(self.spatial_normalization, DartelSpatialNormalization):
      self.spatial_normalization.setDartelTemplatePath(dartel_template_path)
    else:
      raise Exception('Dartel template is only needed for DartelSpatialNormalization')
    
  def setSPMDefaultSpatialNormalization(self):
    del self.spatial_normalization
    self.spatial_normalization = SPMDefaultSpatialNormalization()
    
  def unsetSANLMDenoising(self):
    """
    This  function  applies  an spatial adaptive non local means denoising filter to the data. This
    filter  will  remove  noise  while  preserving edges. The smoothing filter size is automatically
    estimated based on the local variance in the image.
    """
    self.SANLM_denoising_filter = 0
    
  def setSANLMDenoising(self):
    """
    This  function  applies  an spatial adaptive non local means denoising filter to the data. This
    filter  will  remove  noise  while  preserving edges. The smoothing filter size is automatically
    estimated based on the local variance in the image.
    """
    self.SANLM_denoising_filter = 1
    
  def setSANLMDenoisingToMultiThreaded(self):
    """
    This  function  applies  an spatial adaptive non local means denoising filter to the data. This
    filter  will  remove  noise  while  preserving edges. The smoothing filter size is automatically
    estimated based on the local variance in the image.
    """
    self.SANLM_denoising_filter = 2
  
  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)  
  def setMRFWeighting(self, mrf_weighting):
    """
    A  Hidden  Markov  Random  Field  (HMRF)  is  used  to encode spatial information through
    spatial constraints of neighboring voxels (Zhang et al. IEEE TMI 2001). Neighboring voxels
    are  expected  to  have  the  same  class  labels.  The  prior probability of the class and the
    likelihood  probability of the observation is combined to estimate the Maximum a posteriori
    (MAP).  It  is  not  necessary  to  change  the  MRF weighting, because the ORNLM filter will
    have a much larger de-noising effect. A value of "0" will deselect the MRF.
    """
    self.mrf_weighting = mrf_weighting
    
  def unsetCleanUp(self):
    """
    This  uses  a  crude  routine  for  extracting the brain from segmentedimages. It begins by
    taking  the  white  matter, and eroding it acouple of times to get rid of any odd voxels. The
    algorithmcontinues on to do conditional dilations for several iterations,where the condition
    is  based  upon  gray  or  white  matter being present.This identified region is then used to
    clean  up  the  grey  and  whitematter  partitions,  and  has  a  slight influences on the CSF
    partition.
    """
    self.cleanup = 0
    
  def setCleanUpToLight(self):
    """
    This  uses  a  crude  routine  for  extracting the brain from segmentedimages. It begins by
    taking  the  white  matter, and eroding it acouple of times to get rid of any odd voxels. The
    algorithmcontinues on to do conditional dilations for several iterations,where the condition
    is  based  upon  gray  or  white  matter being present.This identified region is then used to
    clean  up  the  grey  and  whitematter  partitions,  and  has  a  slight influences on the CSF
    partition.
    """
    self.cleanup = 1
    
  def setCleanUpToThorough(self):
    """
    This  uses  a  crude  routine  for  extracting the brain from segmentedimages. It begins by
    taking  the  white  matter, and eroding it acouple of times to get rid of any odd voxels. The
    algorithmcontinues on to do conditional dilations for several iterations,where the condition
    is  based  upon  gray  or  white  matter being present.This identified region is then used to
    clean  up  the  grey  and  whitematter  partitions,  and  has  a  slight influences on the CSF
    partition.
    """
    self.cleanup = 2
    
  def enableDisplayAndPrintResult(self):
    """
    The  normalized T1 image and the normalized segmentations can be displayed and printed
    to  a  ps-file.  This  is  often  helpful  to  check whether registration and segmentation were
    successful. However, this is only working if you write normalized images.
    """
    self.print_result = 1
  
  def disableDisplayAndPrintResult(self):
    """
    The  normalized T1 image and the normalized segmentations can be displayed and printed
    to  a  ps-file.  This  is  often  helpful  to  check whether registration and segmentation were
    successful. However, this is only working if you write normalized images.
    """
    self.print_result = 0 
    
  def getStringListForBatch(self):
    batch_list = []
    batch_list.extend(addBatchKeyWordInEachItem("extopts", self.spatial_normalization.getStringListForBatch()))
    batch_list.append("extopts.sanlm = %s;" % self.SANLM_denoising_filter)
    batch_list.append("extopts.mrf = %s;" % self.mrf_weighting)
    batch_list.append("extopts.cleanup = %s;" % self.cleanup)
    batch_list.append("extopts.print = %s;" % self.print_result)
    return batch_list
    
#========================================================================
class DartelSpatialNormalization():
  def __init__(self):
    self.dartel_template_path = None
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setDartelTemplatePath(self, dartel_template_path):
    self.dartel_template_path = dartel_template_path
  
  def getStringListForBatch(self):
    if self.dartel_template_path is not None:
      return ["dartelwarp.normhigh.darteltpm = {'%s'};" % self.dartel_template_path]
    else:
      raise ValueError('dartel template path is required')
    
#========================================================================
class SPMDefaultSpatialNormalization():
  def __init__(self):
    pass
  
  def getStringListForBatch(self):
    return ["dartelwarp.normlow = struct([]);"]