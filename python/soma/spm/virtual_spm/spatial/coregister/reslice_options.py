# -*- coding: utf-8 -*-
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
from soma.spm.spm_batch_maker_utils import convertlistToSPMString

class ResliceOptions():
  """
  Various reslicing options.
  """
    #===========================================================================       
  def setInterpolationToNearestNeighbour(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    Nearest   Neighbour  is  fastest,  but  not  normally  recommended.  It  can  be  useful  for
    re-orienting  images  while  preserving  the  original  intensities (e.g. an image consisting of
    labels).
    """
    self.interpolation = 0
    
  def setInterpolationToTrilinear(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    labels).  Bilinear  Interpolation  is  OK  for  PET,  or  realigned  and  re-sliced fMRI. If subject
    movement  (from  an  fMRI  time  series)  is included in the transformations then it may be
    better  to  use  a higher degree approach.
    """
    self.interpolation = 1
    
  def setInterpolationTo2ndDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    If subject movement  (from  an  fMRI  time  series)  is included in the transformations then 
    it may be better  to  use  a higher degree approach. Note that higher degree B-spline interpolation 
    is slower because it uses more neighbours.
    """
    self.interpolation = 2
    
  def setInterpolationTo3rdDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    If subject movement  (from  an  fMRI  time  series)  is included in the transformations then 
    it may be better  to  use  a higher degree approach. Note that higher degree B-spline interpolation 
    is slower because it uses more neighbours.
    """
    self.interpolation = 3
    
  def setInterpolationTo4thDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    If subject movement  (from  an  fMRI  time  series)  is included in the transformations then 
    it may be better  to  use  a higher degree approach. Note that higher degree B-spline interpolation 
    is slower because it uses more neighbours.
    """
    self.interpolation = 4
    
  def setInterpolationTo5thDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    If subject movement  (from  an  fMRI  time  series)  is included in the transformations then 
    it may be better  to  use  a higher degree approach. Note that higher degree B-spline interpolation 
    is slower because it uses more neighbours.
    """
    self.interpolation = 5
    
  def setInterpolationTo6thDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    If subject movement  (from  an  fMRI  time  series)  is included in the transformations then 
    it may be better  to  use  a higher degree approach. Note that higher degree B-spline interpolation 
    is slower because it uses more neighbours.
    """
    self.interpolation = 6
    
  def setInterpolationTo7thDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    If subject movement  (from  an  fMRI  time  series)  is included in the transformations then 
    it may be better  to  use  a higher degree approach. Note that higher degree B-spline interpolation 
    is slower because it uses more neighbours.
    """
    self.interpolation = 7
    
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
    #===========================================================================    
  def getCurrentFilenamePrefix(self):
    return self.filename_prefix      

  def getStringListForBatch(self):
    batch_list = []
    batch_list.append("roptions.interp = %i;" % self.interpolation)
    batch_list.append("roptions.wrap = %s;" % convertlistToSPMString(self.wrapping))
    batch_list.append("roptions.mask = %i;" % self.masking)
    batch_list.append("roptions.prefix = '%s';" % self.filename_prefix)
    return batch_list
    