# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm_batch_maker_utils import convertlistToSPMString
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode


class ResliceOptions(object):
  """
  Various reslicing options. If in doubt, simply keep the default values.
  """
  def setReslicedImagesToAllImages(self):
    """
    All  Images  (1..n)  :     This reslices all the images - including the first image selected   - which will remain in its original
    position.
    """
    self.resliced_images = [2, 0]
    
  def setReslicedImagesToImagesExceptFirst(self):
    """
    Images  2..n :    Reslices images 2..n only. Useful for if you wish to reslice    (for example) a PET image to fit a structural
    MRI, without    creating a second identical MRI volume.
    """
    self.resliced_images = [1, 0]
    
  def setReslicedImagesToAllImagesAndMeanImage(self):
    """
    All Images + Mean Image :    In addition to reslicing the images, it also creates a mean of the    resliced image.
    """
    self.resliced_images = [2, 1]
    
  def setReslicedImagesToMeanImageOnly(self):
    """
    Mean Image Only :    Creates the mean resliced image only.
    """
    self.resliced_images = [0, 1]


  def setInterpolationToNearestNeighbour(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    Nearest   Neighbour  is  fastest,  but  not  normally  recommended. Voxel sizes must all be 
    identical and isotropic.
    """
    self.interpolation = '0'
    
  def setInterpolationToTrilinear(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    Bilinear  Interpolation  is  probably OK for PET, but not so suitable for fMRI
    because  higher  degree  interpolation  generally  gives  better  results. Voxel sizes must all be 
    identical and isotropic.
    """
    self.interpolation = '1'
    
  def setInterpolationTo2ndDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    for fMRI higher  degree  interpolation  generally  gives  better  results.  Although  higher  degree methods provide better
    interpolation,  but  they  are  slower because they use more neighbouring voxels. Voxel sizes must all be 
    identical and isotropic.
    """
    self.interpolation = '2'
    
  def setInterpolationTo3rdDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    for fMRI higher  degree  interpolation  generally  gives  better  results.  Although  higher  degree methods provide better
    interpolation,  but  they  are  slower because they use more neighbouring voxels. Voxel sizes must all be 
    identical and isotropic.
    """
    self.interpolation = '3'
    
  def setInterpolationTo4thDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    for fMRI higher  degree  interpolation  generally  gives  better  results.  Although  higher  degree methods provide better
    interpolation,  but  they  are  slower because they use more neighbouring voxels. Voxel sizes must all be 
    identical and isotropic.
    """
    self.interpolation = '4'
    
  def setInterpolationTo5thDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    for fMRI higher  degree  interpolation  generally  gives  better  results.  Although  higher  degree methods provide better
    interpolation,  but  they  are  slower because they use more neighbouring voxels. Voxel sizes must all be 
    identical and isotropic.
    """
    self.interpolation = '5'
    
  def setInterpolationTo6thDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    for fMRI higher  degree  interpolation  generally  gives  better  results.  Although  higher  degree methods provide better
    interpolation,  but  they  are  slower because they use more neighbouring voxels. Voxel sizes must all be 
    identical and isotropic.
    """
    self.interpolation = '6'
    
  def setInterpolationTo7thDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    for fMRI higher  degree  interpolation  generally  gives  better  results.  Although  higher  degree methods provide better
    interpolation,  but  they  are  slower because they use more neighbouring voxels. Voxel sizes must all be 
    identical and isotropic.
    """
    self.interpolation = '7'
    
  def setInterpolationToFourierInterpolation(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    Fourier Interpolation is another option, but  note  that  it  is  only  implemented  for  purely  rigid  body  transformations.
    Voxel sizes must all be identical and isotropic.
    """
    self.interpolation = "Inf"
    
  @checkIfArgumentTypeIsAllowed(bool, 1)
  @checkIfArgumentTypeIsAllowed(bool, 2)
  @checkIfArgumentTypeIsAllowed(bool, 3)
  def setWrapping(self, X=True, Y=True, Z=True):
    """
    These are typically:
        No  wrapping - for PET or images that have already been spatially transformed.
        Wrap in Y - for (un-resliced) MRI where phase encoding is in the Y direction (voxel space).
    """
    self.wrapping = [int(X), int(Y), int(Z)]
    
  def setMasking(self):
    """
    Because  of  subject  motion, different images are likely to have different patterns of zeros
    from  where  it  was  not  possible  to  sample  data.  With  masking  enabled, the program
    searches through the whole time series looking for voxels which need to be sampled from
    outside  the  original images. Where this occurs, that voxel is set to zero for the whole set
    of  images  (unless  the  image  format  can  represent  NaN, in which case NaNs are used
    where possible).
    """
    self.masking = 1
    
  def unsetMasking(self):
    """
    Because  of  subject  motion, different images are likely to have different patterns of zeros
    from  where  it  was  not  possible  to  sample  data.  With  masking  enabled, the program
    searches through the whole time series looking for voxels which need to be sampled from
    outside  the  original images. Where this occurs, that voxel is set to zero for the whole set
    of  images  (unless  the  image  format  can  represent  NaN, in which case NaNs are used
    where possible).
    """
    self.masking = 0
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setFilenamePrefix(self, filename_prefix):
    self.filename_prefix = filename_prefix 

  def getReslicedImagesChoices(self):
    return self.resliced_images
  
  def getCurrentFilenamePrefix(self):
    return self.filename_prefix 
  
  def getStringListForBatch(self):
    batch_list = []
    batch_list.append("roptions.which = %s;" % convertlistToSPMString(self.resliced_images))
    batch_list.append("roptions.interp = %s;" % self.interpolation)    
    batch_list.append("roptions.wrap = %s;" % convertlistToSPMString(self.wrapping))
    batch_list.append("roptions.mask = %i;" % self.masking)
    batch_list.append("roptions.prefix = '%s';" % self.filename_prefix)
    return batch_list
