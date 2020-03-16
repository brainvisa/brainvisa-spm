# -*- coding: utf-8 -*-
class Options(object):
  """
  Options for image calculator
  """
  def setDataMatrix(self):
    """
    If the dmtx flag is set, then images are read into a data matrix X (rather than into
    separate  variables  i1,  i2, i3,...). The data matrix  should be referred to as X, and
    contains images in rows. Computation is plane by plane, so in data-matrix mode,
    X  is  a NxK matrix, where N is the number of input images [prod(size(Vi))], and K
    is the number of voxels per plane [prod(Vi(1).dim(1:2))].
    """
    self.data_matrix = 1
    
  def unsetDataMatrix(self):
    """
    If the dmtx flag is set, then images are read into a data matrix X (rather than into
    separate  variables  i1,  i2, i3,...). The data matrix  should be referred to as X, and
    contains images in rows. Computation is plane by plane, so in data-matrix mode,
    X  is  a NxK matrix, where N is the number of input images [prod(size(Vi))], and K
    is the number of voxels per plane [prod(Vi(1).dim(1:2))].
    """
    self.data_matrix = 0
    
  def setMaskingTypeToNoImplicitZero(self):
    """
    For  data  types  without a representation of NaN, implicit zero masking assumes
    that  all  zero  voxels are to be treated as missing, and treats them as NaN. NaN's
    are  written as zero (by spm_write_plane), for data types without a representation
    of NaN.
    One of the following options is available:
    * No implicit zero mask
    * Implicit zero mask
    * NaNs should be zeroed
    """
    self.masking_type = 0
    
  def setMaskingTypeToImplicitZero(self):
    """
    For  data  types  without a representation of NaN, implicit zero masking assumes
    that  all  zero  voxels are to be treated as missing, and treats them as NaN. NaN's
    are  written as zero (by spm_write_plane), for data types without a representation
    of NaN.
    One of the following options is available:
    * No implicit zero mask
    * Implicit zero mask
    * NaNs should be zeroed
    """
    self.masking_type = 1
    
  def setMaskingTypeToNaNShouldBeZeroed(self):
    """
    For  data  types  without a representation of NaN, implicit zero masking assumes
    that  all  zero  voxels are to be treated as missing, and treats them as NaN. NaN's
    are  written as zero (by spm_write_plane), for data types without a representation
    of NaN.
    One of the following options is available:
    * No implicit zero mask
    * Implicit zero mask
    * NaNs should be zeroed
    """
    self.masking_type = 2
    
  def setInterpolationToNearestNeighbour(self):
    """
    With  images  of  different  sizes  and orientations, the size and orientation of the
    first is used for the output image. A warning is given in this situation. Images are
    sampled   into   this  orientation  using  the  interpolation  specified  by  the  hold
    parameter.
    """
    self.interpolation = 0
    
  def setInterpolationToTrilinear(self):
    """
    With  images  of  different  sizes  and orientations, the size and orientation of the
    first is used for the output image. A warning is given in this situation. Images are
    sampled   into   this  orientation  using  the  interpolation  specified  by  the  hold
    parameter.
    """
    self.interpolation = 1
    
  def setInterpolationTo2ndDegreeBSpline(self):
    """
    With  images  of  different  sizes  and orientations, the size and orientation of the
    first is used for the output image. A warning is given in this situation. Images are
    sampled   into   this  orientation  using  the  interpolation  specified  by  the  hold
    parameter.
    """
    self.interpolation = 2
    
  def setInterpolationTo3rdDegreeBSpline(self):
    """
    With  images  of  different  sizes  and orientations, the size and orientation of the
    first is used for the output image. A warning is given in this situation. Images are
    sampled   into   this  orientation  using  the  interpolation  specified  by  the  hold
    parameter.
    """
    self.interpolation = 3
    
  def setInterpolationTo4thDegreeBSpline(self):
    """
    With  images  of  different  sizes  and orientations, the size and orientation of the
    first is used for the output image. A warning is given in this situation. Images are
    sampled   into   this  orientation  using  the  interpolation  specified  by  the  hold
    parameter.
    """
    self.interpolation = 4
    
  def setInterpolationTo5thDegreeBSpline(self):
    """
    With  images  of  different  sizes  and orientations, the size and orientation of the
    first is used for the output image. A warning is given in this situation. Images are
    sampled   into   this  orientation  using  the  interpolation  specified  by  the  hold
    parameter.
    """
    self.interpolation = 5
    
  def setInterpolationTo6thDegreeBSpline(self):
    """
    With  images  of  different  sizes  and orientations, the size and orientation of the
    first is used for the output image. A warning is given in this situation. Images are
    sampled   into   this  orientation  using  the  interpolation  specified  by  the  hold
    parameter.
    """
    self.interpolation = 6
    
  def setInterpolationTo7thDegreeBSpline(self):
    """
    With  images  of  different  sizes  and orientations, the size and orientation of the
    first is used for the output image. A warning is given in this situation. Images are
    sampled   into   this  orientation  using  the  interpolation  specified  by  the  hold
    parameter.
    """
    self.interpolation = 7
    
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
    
  def getStringListForBatch( self ):
    batch_list = []
    batch_list.append("options.dmtx = %i;" %self.data_matrix)
    batch_list.append("options.mask = %i;" %self.masking_type)
    batch_list.append("options.interp = %i;" %self.interpolation)
    batch_list.append("options.dtype = %i;" %self.data_type)
    return batch_list