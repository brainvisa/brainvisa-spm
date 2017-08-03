# -*- coding: utf-8 -*-
from soma.spm.spm_batch_maker_utils import moveSPMPath, convertlistToSPMString
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
import numbers

class Smooth():
  """
  This  is  for smoothing (or convolving) image volumes with a Gaussian kernel of a
  specified  width.  It is used as a preprocessing step to suppress noise and effects
  due  to  residual  differences in functional and gyral anatomy during inter-subject
  averaging.
  """

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setInputImagePathList(self, image_path_list):
    """
    Specify  the  images  to  smooth.  The  smoothed images are written to the same
    subdirectories as the original images and are prefixed with a 's'. The prefix can be
    changed by an option setting.
    """
    self.input_path_list = image_path_list

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setOutputImagePathList(self, image_path_list):
    """
    Specify  the  images output path if you don't want to use the SPM prefix
    """
    self.output_path_list = image_path_list

  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
  @checkIfArgumentTypeIsAllowed(numbers.Real, 2)
  @checkIfArgumentTypeIsAllowed(numbers.Real, 3)
  def setFWHM(self, x, y ,z):
    """
    Specify the full-width at half maximum (FWHM) of the Gaussian smoothing kernel
    in  mm.  Three  values  should  be  entered,  denoting the FWHM in the x, y and z
    directions.
    """
    self.fwhm = convertlistToSPMString([x, y, z])

  def setDataTypeToSame(self):
    """
    Data-type  of  output  images.   SAME indicates the same datatype as the original
    images.
    """
    self.data_type = 0

  def setDataTypeToUint8(self):
    """
    Data-type of output image
    """
    self.data_type = 2

  def setDataTypeToInt16(self):
    """
    Data-type of output image
    """
    self.data_type = 4

  def setDataTypeToInt32(self):
    """
    Data-type of output image
    """
    self.data_type = 8

  def setDataTypeToFloat32(self):
    """
    Data-type of output image
    """
    self.data_type = 16

  def setDataTypeToFloat64(self):
    """
    Data-type of output image
    """
    self.data_type = 64

  def unsetImplicitMasking(self):
    """
    An  "implicit  mask"  is  a  mask  implied by a particular voxel value (0 for images
    with integer type, NaN for float images).
    If  set,  the  implicit  masking  of  the  input  image  is  preserved  in the
    smoothed image.
    """
    self.implicit_masking = 0

  def setImplicitMasking(self):
    """
    An  "implicit  mask"  is  a  mask  implied by a particular voxel value (0 for images
    with integer type, NaN for float images).
    If  set,  the  implicit  masking  of  the  input  image  is  preserved  in the
    smoothed image.
    """
    self.implicit_masking = 1

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setFilenamePrefix(self, filename_prefix):
    self.filename_prefix = filename_prefix

  def getStringListForBatch( self ):
    if not None in [self.input_path_list]:
      batch_list = []
      image_path_list_for_batch = []
      for image_path in self.input_path_list:
        image_path_list_for_batch.append("'%s,1'" % image_path)
      image_path_for_batch = '\n'.join(image_path_list_for_batch)

      batch_list.append("spm.spatial.smooth.data = {%s};" %image_path_for_batch)
      batch_list.append("spm.spatial.smooth.fwhm = %s;" %self.fwhm)
      batch_list.append("spm.spatial.smooth.dtype = %i;" %self.data_type)
      batch_list.append("spm.spatial.smooth.im = %i;" %self.implicit_masking)
      batch_list.append("spm.spatial.smooth.prefix = '%s';" %self.filename_prefix)
      return batch_list
    else:
      raise ValueError("At least one input_path is mandatory")

  def _moveSPMDefaultPathsIfNeeded(self):
    if self.output_path_list is not None:
      if len(self.input_path_list) == len(self.output_path_list):
        for input_path, output_path in zip(self.input_path_list,
                                           self.output_path_list):
          moveSPMPath(input_path,
                      output_path,
                      prefix=self.filename_prefix)
      else:
        raise ValueError("input_path_list has not the same length than output_path_list")
    else:
      pass#default prefix used
