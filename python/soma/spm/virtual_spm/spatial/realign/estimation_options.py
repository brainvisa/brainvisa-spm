# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm_batch_maker_utils import convertlistToSPMString
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
import numbers

class EstimationOptions(object):
  """
  Various registration options. If in doubt, simply keep the default values.
  """

  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)  
  def setQuality(self, quality):
    """
    Quality  versus  speed  trade-off.    Highest  quality  (1)  gives most precise results, whereas lower qualities gives faster
    realignment.  The  idea  is  that  some  voxels  contribute  little  to  the  estimation  of the realignment parameters. This
    parameter is involved in selecting the number of voxels that are used.
    """
    self.quality = quality

  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)  
  def setSeparation(self, separation):
    """
    The  separation  (in  mm)  between  the  points  sampled in the reference image.  Smaller sampling distances gives more
    accurate results, but will be slower.
    """
    self.separation = separation
    
  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)  
  def setSmoothingFWHM(self, fwhm):
    """
    The FWHM of the Gaussian smoothing kernel (mm) applied to the images before estimating the realignment parameters.
        * PET images typically use a 7 mm kernel.
        * MRI images typically use a 5 mm kernel.
    """
    self.fwhm = fwhm
    
  def setNumPassesToRegisterToFirst(self):
    """
    Register  to first: Images are registered to the first image in the series. R
    MRI  images  are  typically  registered  to the first image.  The more accurate way would be to use a two pass procedure,
    but this probably wouldn't improve the results so much and would take twice as long to run.
    """
    self.num_passes = 0
    
  def setNumPassesToRegisterToMean(self):
    """
    egister to mean:   A two pass procedure is used in order to register the images to the mean of the images after the first realignment.
    PET  images  are  typically registered to the mean. This is because PET data are more noisy than fMRI and there are fewer
    of them, so time is less of an issue.
    """
    self.num_passes = 1
  
  def setInterpolationToTrilinear(self):
    """
    The method by which the images are sampled when estimating the optimum transformation. Higher degree interpolation
    methods provide the better interpolation, but they are slower because they use more neighbouring voxels .
    """
    self.interpolation = 1
    
  def setInterpolationTo2ndDegreeBSpline(self):
    """
    The method by which the images are sampled when estimating the optimum transformation. Higher degree interpolation
    methods provide the better interpolation, but they are slower because they use more neighbouring voxels .
    """
    self.interpolation = 2
    
  def setInterpolationTo3rdDegreeBSpline(self):
    """
    The method by which the images are sampled when estimating the optimum transformation. Higher degree interpolation
    methods provide the better interpolation, but they are slower because they use more neighbouring voxels .
    """
    self.interpolation = 3
    
  def setInterpolationTo4thDegreeBSpline(self):
    """
    The method by which the images are sampled when estimating the optimum transformation. Higher degree interpolation
    methods provide the better interpolation, but they are slower because they use more neighbouring voxels .
    """
    self.interpolation = 4
    
  def setInterpolationTo5thDegreeBSpline(self):
    """
    The method by which the images are sampled when estimating the optimum transformation. Higher degree interpolation
    methods provide the better interpolation, but they are slower because they use more neighbouring voxels .
    """
    self.interpolation = 5
    
  def setInterpolationTo6thDegreeBSpline(self):
    """
    The method by which the images are sampled when estimating the optimum transformation. Higher degree interpolation
    methods provide the better interpolation, but they are slower because they use more neighbouring voxels .
    """
    self.interpolation = 6
    
  def setInterpolationTo7thDegreeBSpline(self):
    """
    The method by which the images are sampled when estimating the optimum transformation. Higher degree interpolation
    methods provide the better interpolation, but they are slower because they use more neighbouring voxels .
    """
    self.interpolation = 7
  
  @checkIfArgumentTypeIsAllowed(bool, 1)
  @checkIfArgumentTypeIsAllowed(bool, 2)
  @checkIfArgumentTypeIsAllowed(bool, 3)
  def setWrapping(self, X=True, Y=True, Z=True):
    """
    This indicates which directions in the volumes the values should wrap around in.  For example, in MRI scans, the images
    wrap  around  in  the  phase  encode direction, so (e.g.) the subject's nose may poke into the back of the subject's head.
    These are typically:
        No  wrapping - for PET or images that have already been spatially transformed.
        Wrap in Y - for (un-resliced) MRI where phase encoding is in the Y direction (voxel space).
    """
    self.wrapping = [int(X), int(Y), int(Z)]
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setWeighting(self, weighting_image_path):
    """
    The  option  of  providing a weighting image to weight each voxel of the reference image differently when estimating the
    realignment  parameters.    The  weights are proportional to the inverses of the standard deviations. This would be used,
    for  example,  when  there  is  a  lot of extra-brain motion - e.g., during speech, or when there are serious artifacts in a
    particular region of the images.
    """
    self.weighting_image_path = weighting_image_path
        
  def getStringListForBatch(self):
    batch_list = []
    batch_list.append("eoptions.quality = %g;" % self.quality)
    batch_list.append("eoptions.sep = %g;" % self.separation)
    batch_list.append("eoptions.fwhm = %g;" % self.fwhm)
    batch_list.append("eoptions.rtm = %i;" % self.num_passes)
    batch_list.append("eoptions.interp = %i;" % self.interpolation)
    batch_list.append("eoptions.wrap = %s;" % convertlistToSPMString(self.wrapping))
    batch_list.append("eoptions.weight = '%s';" % self.weighting_image_path)
    return batch_list
