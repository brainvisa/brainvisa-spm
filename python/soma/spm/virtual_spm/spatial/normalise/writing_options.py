 # -*- coding: utf-8 -*- 
from soma.spm.spm_batch_maker_utils import convertNumpyArrayToSPMString, convertlistToSPMString
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode

class WritingOptions():
  """
  Various options for writing normalised images.
  """
  def setPreserveToConcentrations(self):
    """
    Preserve  Concentrations:  Spatially  normalised  images  are not "modulated". The
    warped images preserve the intensities of the original images.
    """
    self.preserve = 0
    
  def setPreserveToAmount(self):
    """
    Preserve  Total:  Spatially  normalised images are "modulated" in order to preserve
    the  total amount of signal in the images. Areas that are expanded during warping
    are correspondingly reduced in intensity.
    """
    self.preserve = 1
  
  def setBoundingBox(self, numpy_array):
    """
    The  bounding  box  (in  mm)  of the volume which is to be written (relative to the
    anterior commissure).
    """
    if numpy_array.shape == (2, 3):
      self.bounding_box = numpy_array
    else:
      raise ValueError("An 2-by-3 array must be entered")
    
  def setVoxelSize(self, voxel_size_list):
    """
    The voxel sizes (x, y & z, in mm) of the written normalised images.
    """
    if len(voxel_size_list) == 3:
      self.voxel_size = voxel_size_list
    else:
      raise ValueError("voxel_size_list must have 3 items [x, y, z]")
    
  def setInterpolationToNearestNeighbour(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    Nearest Neighbour:
          - Fastest, but not normally recommended.
    """
    self.interpolation = 0
    
  def setInterpolationToTrilinear(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    Trilinear Interpolation:
          - OK for PET, realigned fMRI, or segmentations
    """
    self.interpolation = 1
    
  def setInterpolationTo2ndDegreeBSpline(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
          - Better  quality (but slower) interpolation, especially with higher degree splines. Can produce
            values  outside  the  original range (e.g. small negative values from an originally all positive
            image).
    """
    self.interpolation = 2
    
  def setInterpolationTo3rdDegreeBSpline(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
          - Better  quality (but slower) interpolation, especially with higher degree splines. Can produce
            values  outside  the  original range (e.g. small negative values from an originally all positive
            image).
    """
    self.interpolation = 3
    
  def setInterpolationTo4thDegreeBSpline(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
          - Better  quality (but slower) interpolation, especially with higher degree splines. Can produce
            values  outside  the  original range (e.g. small negative values from an originally all positive
            image).
    """
    self.interpolation = 4
    
  def setInterpolationTo5thDegreeBSpline(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
          - Better  quality (but slower) interpolation, especially with higher degree splines. Can produce
            values  outside  the  original range (e.g. small negative values from an originally all positive
            image).
    """
    self.interpolation = 5
    
  def setInterpolationTo6thDegreeBSpline(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
          - Better  quality (but slower) interpolation, especially with higher degree splines. Can produce
            values  outside  the  original range (e.g. small negative values from an originally all positive
            image).
    """
    self.interpolation = 6
    
  def setInterpolationTo7thDegreeBSpline(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
          - Better  quality (but slower) interpolation, especially with higher degree splines. Can produce
            values  outside  the  original range (e.g. small negative values from an originally all positive
            image).
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
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setFilenamePrefix(self, filename_prefix):
    """
    Specify  the  string  to  be  prepended  to  the  filenames of the normalised image
    file(s). Default prefix is 'w'.
    """
    self.filename_prefix = filename_prefix
    
  def getStringListForBatch(self):
    batch_list = []
    batch_list.append("roptions.preserve = %i;" %self.preserve)
    batch_list.append("roptions.bb = %s;" %convertNumpyArrayToSPMString(self.bounding_box))
    batch_list.append("roptions.vox = %s;" %convertlistToSPMString(self.voxel_size))
    batch_list.append("roptions.interp = %i;" %self.interpolation)
    batch_list.append("roptions.wrap = %s;" %convertlistToSPMString(self.wrapping))
    batch_list.append("roptions.prefix = '%s';" %self.filename_prefix)
    return batch_list
  
  def getCurrentFilenamePrefix(self):
    return self.filename_prefix