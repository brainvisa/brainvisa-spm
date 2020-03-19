# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsStrOrUnicode, checkIfArgumentTypeIsAllowed
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem,\
  convertlistToSPMString, convertPathListToSPMBatchString,\
  convertNumpyArrayToSPMString, moveFileAndCreateFoldersIfNeeded,\
  moveSPMPath

import abc
import numbers
import numpy
import os
import six
from six.moves import zip


class Output(six.with_metaclass(abc.ABCMeta)):
  """
  Various  output  options  are  available.    The  deformation  may  be  saved to disk as a ``y_*.nii'' file.Images may be
  warped  using  the  resulting deformation, either using a ``pullback'' procedure, or a ``pushforward''.The old style of
  spatial normalisation involved the pullback, whereas the pushforward requires the inverse of the deformation used by
  the pullback.  Finally, the deformation may be used to warp a GIFTI surface file.
  """
  pass

#===============================================================================
# 
#===============================================================================
class SaveDeformation(Output):
  """
  The deformation may be saved to disk as a ``y_*.nii'' file.
  """
  def __init__(self):
    self.deformation_name = ''
    self.output_destination = OutputDestination()
    
    self.deformation_saved_path = None
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setDeformationName(self, deformation_name):
    """
    Save the result as a three-volume image.  "y_" will be prepended to the filename.
    """
    self.deformation_name = deformation_name
    
  def setOutputDestinationToCurrentDirectory(self):
    self.output_destination.setOutputDestinationToCurrentDirectory()
    
  def setOutputDestinationToOutputDirectory(self, ouput_directory):
    self.output_destination.setOutputDestinationToOutputDirectory(ouput_directory)
    
  def getStringListForBatch( self ):
    if self.current_directory or self.ouput_directory is not None:
      batch_list = []
      batch_list.append("savedef.ofname = '%s';" %self.deformation_name)
      batch_list.extend(addBatchKeyWordInEachItem("savedef", self.output_destination.getStringListForBatch()))
      return batch_list
    else:
      raise ValueError("ouput directory path is required if output destination is not current directory")
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setOuputDeformationPath(self, deformation_saved_path):
    self.deformation_saved_path = deformation_saved_path
    
  def _moveSPMDefaultPathsIfNeeded(self):
    if self.deformation_saved_path is not None:
      ouput_directory = self.output_destination.getOutputDirectory()
      spm_default_output_path = os.path.join(ouput_directory, 'y_'+self.deformation_name)
      moveFileAndCreateFoldersIfNeeded(spm_default_output_path, self.deformation_saved_path)
    else:
      pass#default spm outputs used
#===============================================================================
# 
#===============================================================================
class PullBack(Output):
  """
  This is the old way of warping images, which involves resampling images based on a mapping from the new (warped)
  image  space  back  to  the  original image.  The deformation should be the inverse of the deformation that would be
  used for the pushforward procedure.
  """
  def __init__(self):
    self.volume_list_to_apply = None
    self.output_destination = OutputDestinationWithSources()     
    self.interpolation = 4
    self.gaussian_fwhm = [0, 0, 0]   
    
    self.ouput_path_list = None
    
  @checkIfArgumentTypeIsAllowed(list, 1)  
  def setVolumeListToApply(self, volume_list_to_apply):
    self.volume_list_to_apply = volume_list_to_apply
    
  def setOutputDestinationToCurrentDirectory(self):
    self.output_destination.setOutputDestinationToCurrentDirectory()
    
  def setOuputDestinationToSourceDirectories(self):
    self.output_destination.setOuputDestinationToSourceDirectories()
    
  def setOutputDestinationToOutputDirectory(self, ouput_directory):
    self.output_destination.setOutputDestinationToOutputDirectory(ouput_directory)
    
  def setInterpolationToNearestNeighbour(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    (Note that Inf or NaN values are treated as zero, rather than as missing data)
    Nearest Neighbour:
    - Fastest, but not normally recommended.
    """
    self.interpolation = 0
    
  def setInterpolationToTrilinear(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    (Note that Inf or NaN values are treated as zero, rather than as missing data)
    Trilinear Interpolation:
    - OK for PET, realigned fMRI, or segmentations
    """
    self.interpolation = 1
    
  def setInterpolationTo2ndDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    (Note that Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
    - Better  quality  (but  slower)  interpolation,  especially with higher degree splines. Can
      produce   values   outside  the  original  range  (e.g.  small  negative  values  from  an
      originally all positive image).
    """
    self.interpolation = 2
    
  def setInterpolationTo3rdDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    (Note that Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
    - Better  quality  (but  slower)  interpolation,  especially with higher degree splines. Can
      produce   values   outside  the  original  range  (e.g.  small  negative  values  from  an
      originally all positive image).
    """
    self.interpolation = 3
    
  def setInterpolationTo4thDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    (Note that Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
    - Better  quality  (but  slower)  interpolation,  especially with higher degree splines. Can
      produce   values   outside  the  original  range  (e.g.  small  negative  values  from  an
      originally all positive image).
    """
    self.interpolation = 4
    
  def setInterpolationTo5thDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    (Note that Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
    - Better  quality  (but  slower)  interpolation,  especially with higher degree splines. Can
      produce   values   outside  the  original  range  (e.g.  small  negative  values  from  an
      originally all positive image).
    """
    self.interpolation = 5
    
  def setInterpolationTo6thDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    (Note that Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
    - Better  quality  (but  slower)  interpolation,  especially with higher degree splines. Can
      produce   values   outside  the  original  range  (e.g.  small  negative  values  from  an
      originally all positive image).
    """
    self.interpolation = 6
    
  def setInterpolationTo7thDegreeBSpline(self):
    """
    The  method  by  which  the  images  are  sampled when being written in a different space.
    (Note that Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
    - Better  quality  (but  slower)  interpolation,  especially with higher degree splines. Can
      produce   values   outside  the  original  range  (e.g.  small  negative  values  from  an
      originally all positive image).
    """
    self.interpolation = 7
    
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
    
  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)  
  @checkIfArgumentTypeIsAllowed(numbers.Real, 2)  
  @checkIfArgumentTypeIsAllowed(numbers.Real, 3)  
  def setFWHM(self, x, y ,z):
    """
    Specify the full-width at half maximum (FWHM) of the Gaussian smoothing kernel
    in  mm.  Three  values  should  be  entered,  denoting the FWHM in the x, y and z
    directions.
    """
    self.fwhm = [x, y, z]
    
  def getStringListForBatch( self ):
    if self.volume_list_to_apply is not None:
      batch_list = []
      batch_list.append("pull.fnames = {%s};"%convertPathListToSPMBatchString(self.volume_list_to_apply,
                                                                              add_dimension=False))
      batch_list.extend(addBatchKeyWordInEachItem("pull", self.output_destination.getStringListForBatch()))
      batch_list.append("pull.interp = %i;"%self.interpolation)
      batch_list.append("pull.mask = %i;"%self.masking)
      batch_list.append("pull.fwhm = %s;"%convertlistToSPMString(self.gaussian_fwhm))
      return batch_list
    else:
      raise ValueError("volume list to apply is required")
    
  @checkIfArgumentTypeIsAllowed(list, 1)  
  def setOuputPathList(self, ouput_path_list):
    self.ouput_path_list = ouput_path_list
    
  def _moveSPMDefaultPathsIfNeeded(self):
    if self.ouput_path_list is not None:
      if len(self.volume_list_to_apply) == len(self.ouput_path_list):
        for input_path, output_path in zip(self.volume_list_to_apply, self.ouput_path_list):
          if self.output_destination.sources:
            moveSPMPath(input_path, output_path, prefix='w')
          else:
            output_directory = self.output_destination.getOutputDirectory()
            spm_default_path = os.path.join(output_directory, 'w' + os.path.basename(input_path))
            moveFileAndCreateFoldersIfNeeded(spm_default_path, output_path)
      else:
        raise ValueError("input and output number mismatch")
    else:
      pass#default spm outputs used
  #===========================================================================
  # 
  #===========================================================================
class PushFoward(Output):
  """
  This is the old way of warping images, which involves resampling images based on a mapping from the new (warped)
  image  space  back  to  the  original image.  The deformation should be the inverse of the deformation that would be
  used for the pushforward procedure.
  """
  def __init__(self):
    self.volume_list_to_apply = None
    self.weight_image_path = ''
    self.output_destination = OutputDestinationWithSources() 
    self.image_defined_path = None
    self.user_defined_bouding_box = None
    self.user_defined_voxel_size = None
    self.preserve = 0
    self.gaussian_fwhm = [0, 0, 0]
    
  @checkIfArgumentTypeIsAllowed(list, 1)  
  def setVolumeListToApply(self, volume_list_to_apply):
    """
    Apply the resulting deformation field to some images. The filenames will be prepended by "w".
    """
    self.volume_list_to_apply = volume_list_to_apply  
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setWeightImagePath(self, weight_image_path):
    """
    Select  an image file to weight the warped data with.  This is optional, but the idea is the same
    as  was  used  by  JE  Lee  et  al  (2009)  in  their  ``A  study  of  diffusion  tensor  imaging by
    tissue-specific, smoothing-compensated voxel-based analysis'' paper.  In principle, a mask of
    (eg)  white  matter  could  be  supplied,  such  that  the warped images contain average signal
    intensities in WM.
    """
    self.weight_image_path = weight_image_path
    
  def setOutputDestinationToCurrentDirectory(self):
    self.output_destination.setOutputDestinationToCurrentDirectory()
    
  def setOuputDestinationToSourceDirectories(self):
    self.output_destination.setOuputDestinationToSourceDirectories()
    
  def setOutputDestinationToOutputDirectory(self, ouput_directory):
    self.output_destination.setOutputDestinationToOutputDirectory(ouput_directory)
    
  def setFieldOfViewToImageDefined(self, image_defined_path):
    """
    Use the dimensions, orientation etc of some pre-existing image.
    """
    self.image_defined_path = image_defined_path
    self.user_defined_bouding_box = None
    self.user_defined_voxel_size = None
    
  @checkIfArgumentTypeIsAllowed(numpy.ndarray, 1)  
  @checkIfArgumentTypeIsAllowed(list, 2)  
  def setFieldOfViewToUserDefined(self, bounding_box, voxel_size_list):
    """
    The  part  of the deformation to use is specified by defining the bounding box and voxel sizes
    that  you  would  like to have. This is probably stating the obvious to many but smaller voxels
    and a broader bounding box will take up more disk space, but may give a little more accuracy.
    """
    if bounding_box.shape == (2, 3):
      self.user_defined_bouding_box = bounding_box
    else:
      raise ValueError("An 2-by-3 array must be entered")
    if len(voxel_size_list) == 3:
      self.user_defined_voxel_size = voxel_size_list
    else:
      raise ValueError("3 values are required for voxel size")
    
    self.image_defined_path = None
    
  def setPreserveToConcentrations(self):
    """
    Preserve  Concentrations:  Smoothed  spatially  normalised  images  (sw*)  represent weighted
    averages of the signal under the smoothing kernel, approximately preserving the intensities of
    the original images. This option is currently suggested for eg fMRI.
    """
    self.preserve = 0
    
  def setPreserveToAmount(self):
    """
    Preserve  Total: Smoothed and spatially normalised images preserve the total amount of signal
    from   each   region  in  the  images  (smw*).  Areas  that  are  expanded  during  warping  are
    correspondingly reduced in intensity. This option is suggested for VBM.
    """
    self.preserve = 1
    
  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)  
  @checkIfArgumentTypeIsAllowed(numbers.Real, 2)  
  @checkIfArgumentTypeIsAllowed(numbers.Real, 3)  
  def setFWHM(self, x, y ,z):
    """
    Specify  the  full-width at half maximum (FWHM) of the Gaussian blurring kernel in mm. Three
    values  should  be  entered, denoting the FWHM in the x, y and z directions. Note that you can
    specify  [0 0 0], but any "modulated" data will show aliasing, which occurs because of the way
    the warped images are generated.
    """
    self.fwhm = [x, y, z]
    
  def getStringListForBatch( self ):
    if self.volume_list_to_apply is not None:
      batch_list = []
      batch_list.append("push.fnames = {%s};"%convertPathListToSPMBatchString(self.volume_list_to_apply,
                                                                              add_dimension=False))
      batch_list.append("pull.weight = {'%s'};"%self.weight_image_path)
      batch_list.extend(addBatchKeyWordInEachItem("push", self.output_destination.getStringListForBatch()))
      if self.image_defined_path is not None:
        batch_list.append("push.fov.file = {'%s'};"%self.image_defined_path)
      elif not None in [self.user_defined_bouding_box, self.user_defined_voxel_size]:
        batch_list.append("push.fov.bbvox.bb = %s;"%convertNumpyArrayToSPMString(self.image_defined_path))
        batch_list.append("push.fov.bbvox.vox = %s;"%convertlistToSPMString(self.image_defined_path))
      else:
        raise ValueError("Unvalid Field of View configuration")
      batch_list.append("push.preserve = %i;"%self.preserve)
      batch_list.append("push.fwhm = %s;"%convertlistToSPMString(self.gaussian_fwhm))
      return batch_list
    else:
      raise ValueError("volume list to apply is required")
    
  @checkIfArgumentTypeIsAllowed(list, 1)  
  def setOuputPathList(self, ouput_path_list):
    self.ouput_path_list = ouput_path_list
    
  def _moveSPMDefaultPathsIfNeeded(self):
    if self.ouput_path_list is not None:
      if len(self.volume_list_to_apply) == len(self.ouput_path_list):
        for input_path, output_path in zip(self.volume_list_to_apply, self.ouput_path_list):
          if self.output_destination.sources:
            moveSPMPath(input_path, output_path, prefix='w')
          else:
            output_directory = self.output_destination.getOutputDirectory()
            spm_default_path = os.path.join(output_directory, 'w' + os.path.basename(input_path))
            moveFileAndCreateFoldersIfNeeded(spm_default_path, output_path)
      else:
        raise ValueError("input and output number mismatch")
    else:
      pass#default spm outputs used
  #===========================================================================
  # 
  #===========================================================================
class Surface(Output):
  """
  Surfaces  may be warped using the resulting deformation. Note that a procedure similar to the
  pushforward  is used, so the deformation should be the inverse of the one that would be used
  for spatially normalising images via the pullback procedure.
  """
  def __init__(self):
    self.surface_path_list = None
    self.output_destination = OutputDestinationWithSources() 
    
  @checkIfArgumentTypeIsAllowed(list, 1)  
  def setSurfacePathList(self, surface_path_list):
    self.surface_path_list = surface_path_list
    
  def setOutputDestinationToCurrentDirectory(self):
    self.output_destination.setOutputDestinationToCurrentDirectory()
    
  def setOuputDestinationToSourceDirectories(self):
    self.output_destination.setOuputDestinationToSourceDirectories()
    
  def setOutputDestinationToOutputDirectory(self, ouput_directory):
    self.output_destination.setOutputDestinationToOutputDirectory(ouput_directory)
    
  def getStringListForBatch( self ):
    if self.surface_path_list is not None:
      batch_list = []
      batch_list.append("surf.surface = {%s};"%convertPathListToSPMBatchString(self.surface_path_list,
                                                                               add_dimension=False))
      batch_list.extend(addBatchKeyWordInEachItem("surf", self.output_destination.getStringListForBatch()))
      return batch_list
    else:
      raise ValueError("surface path list is required")
    
  @checkIfArgumentTypeIsAllowed(list, 1)  
  def setOuputPathList(self, ouput_path_list):
    self.ouput_path_list = ouput_path_list
    
  def _moveSPMDefaultPathsIfNeeded(self):
    if self.ouput_path_list is not None:
      if len(self.surface_path_list) == len(self.ouput_path_list):
        for input_path, output_path in zip(self.surface_path_list, self.ouput_path_list):
          if self.output_destination.sources:
            moveSPMPath(input_path, output_path, prefix='w')
          else:
            output_directory = self.output_destination.getOutputDirectory()
            spm_default_path = os.path.join(output_directory, 'w' + os.path.basename(input_path))
            moveFileAndCreateFoldersIfNeeded(spm_default_path, output_path)
      else:
        raise ValueError("input and output number mismatch")
    else:
      pass#default spm outputs used
#===============================================================================
# 
#===============================================================================
class SaveJacobianDeterminants(Output):
  """
  The Jacobian determinants may be saved to disk as a ``j_*.nii'' file.
  """
  def __init__(self):
    self.output_filename = ''
    self.output_destination = OutputDestination() 
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setOutputFilename(self, output_filename):
    """
    Save the Jacobian determinants as an image.  "j_" will be prepended to the filename.
    """
    self.output_filename = output_filename
    
  def setOutputDestinationToCurrentDirectory(self):
    self.output_destination.setOutputDestinationToCurrentDirectory()
    
  def setOutputDestinationToOutputDirectory(self, ouput_directory):
    self.output_destination.setOutputDestinationToOutputDirectory(ouput_directory)
    
  def getStringListForBatch( self ):
    batch_list = []
    batch_list.append("savejac.ofname = '%s';"%self.output_filename)
    batch_list.extend(addBatchKeyWordInEachItem("savejac", self.output_destination.getStringListForBatch()))
    return batch_list
#===============================================================================
#===============================================================================
# # 
#===============================================================================
#===============================================================================
class OutputDestination(object):
  """
  Output destination
  """
  def __init__(self):
    self.current_directory = True
    self.ouput_directory = None
    
  def setOutputDestinationToCurrentDirectory(self):
    """
    All created files (deformation fields and warped images) are written to the current directory.
    """
    self.current_directory = True
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setOutputDestinationToOutputDirectory(self, ouput_directory):
    """
    The combined deformation field and the warped images are written into the specified directory.
    """
    self.current_directory = False
    self.ouput_directory = ouput_directory
    
  def getStringListForBatch( self ):
    if self.current_directory or self.ouput_directory is not None:
      batch_list = []
      if self.current_directory:
        batch_list.append("savedir.savepwd = 1;")
      else:
        batch_list.append("savedir.saveusr = {'%s'};"%self.ouput_directory)
      return batch_list
    else:
      raise ValueError("ouput directory path is required if output destination is not current directory")
    
  def getOutputDirectory(self):
    if self.current_directory:
      raise NotImplementedError()
    else:
      return self.ouput_directory
  
class OutputDestinationWithSources(object):
  """
  Output destination with sources possibility
  """
  def __init__(self):
    self.current_directory = True
    self.ouput_directory = None
    self.sources = False
    
  def setOutputDestinationToCurrentDirectory(self):
    """
    All created files (deformation fields and warped images) are written to the current directory.
    """
    self.current_directory = True
    self.ouput_directory = None
    self.sources = False
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setOutputDestinationToOutputDirectory(self, ouput_directory):
    """
    The combined deformation field and the warped images are written into the specified directory.
    """
    self.current_directory = False
    self.ouput_directory = ouput_directory
    self.sources = False
    
  def setOuputDestinationToSourceDirectories(self):
    """
    The  combined  deformation  field  is  written  into the directory of the first deformation field
    warped images are written to the same directories as the source images.
    """
    self.current_directory = False
    self.ouput_directory = None
    self.sources = True
    
  def getStringListForBatch( self ):
    if self.current_directory or self.ouput_directory is not None:
      batch_list = []
      if self.current_directory:
        batch_list.append("savedir.savepwd = 1;")
      elif self.sources:
        batch_list.append("savedir.savesrc = 1;")
      else:
        batch_list.append("savedir.saveusr = {'%s'};"%self.ouput_directory)
      return batch_list
    else:
      raise ValueError("ouput directory path is required if output destination is not current directory or sources")
    
  def getOutputDirectory(self):
    if self.ouput_directory is not None:
      return self.ouput_directory
    elif self.sources:
      raise ValueError("output directory depends on sources")
    elif self.current_directory:
      raise NotImplementedError()
    else:
      raise ValueError("Unvalid output directory choice")
