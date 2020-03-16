# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
import six

class Masking(object):
  """
  The mask specifies the voxels within the image volume which are to be assessed.
  SPM  supports  three  methods  of  masking  (1)  Threshold,  (2)  Implicit  and  (3)
  Explicit. The volume analysed is the intersection of all masks.
  """
  def enableImplicitMask(self):
    """
    An  "implicit  mask" is a mask implied by a particular voxel value. Voxels with this
    mask value are excluded from the analysis.
    For  image  data-types  with  a representation of NaN (see spm_type.m), NaN's is
    the implicit mask value, (and NaN's are always masked out).
    For  image  data-types  without  a representation of NaN, zero is the mask value,
    and the user can choose whether zero voxels should be masked out or not.
    By default, an implicit mask is used. 
    """
    self.implicit_mask = True

  def disableImplicitMask(self):
    """
    An  "implicit  mask" is a mask implied by a particular voxel value. Voxels with this
    mask value are excluded from the analysis.
    For  image  data-types  with  a representation of NaN (see spm_type.m), NaN's is
    the implicit mask value, (and NaN's are always masked out).
    For  image  data-types  without  a representation of NaN, zero is the mask value,
    and the user can choose whether zero voxels should be masked out or not.
    By default, an implicit mask is used. 
    """
    self.implicit_mask = False

  def setExplicitMask(self, explicit_mask_path):
    """
    Explicit masks are other images containing (implicit) masks that are to be applied
    to the current analysis.
    All  voxels with value NaN (for image data-types with a representation of NaN), or
    zero (for other data types) are excluded from the analysis.
    Explicit  mask  images  can  have  any  orientation  and voxel/image size. Nearest
    neighbour  interpolation  of a mask image is used if the voxel centers of the input
    images do not coincide with that of the mask image.
    """
    if isinstance(explicit_mask_path, str) or isinstance(explicit_mask_path, six.text_type):
      self.explicit_mask_path = explicit_mask_path
    else:
      raise ValueError('Explicit mask value must be a file path not ' + str(type(explicit_mask_path)))

  def removeExplicitMask(self):
    """
    Explicit masks are other images containing (implicit) masks that are to be applied
    to the current analysis.
    All  voxels with value NaN (for image data-types with a representation of NaN), or
    zero (for other data types) are excluded from the analysis.
    Explicit  mask  images  can  have  any  orientation  and voxel/image size. Nearest
    neighbour  interpolation  of a mask image is used if the voxel centers of the input
    images do not coincide with that of the mask image.
    """
    self.explicit_mask_path = None
  
  def setThresholdMethodToAbsolute(self):
    self.threshold_masking.setThresholdMethodToAbsolute()
    
  def setThresholdMethodToRelative(self):
    self.threshold_masking.setThresholdMethodToRelative()
    
  def unsetThreshold(self):
    self.threshold_masking.unsetThreshold()

  def setThreshold(self, threshold):
    self.threshold_masking.setThreshold( threshold )
    
  def getStringListForBatch( self ):
    batch_list = []
    batch_list.extend(addBatchKeyWordInEachItem("masking", self.threshold_masking.getStringListForBatch()))
    batch_list.append("masking.im = %i;" % self.implicit_mask)
    if self.explicit_mask_path is not None:
      batch_list.append("masking.em = {'%s,1'};" % self.explicit_mask_path)
    else:
      batch_list.append("masking.em = {''};")
    return batch_list

class ThresholdMasking(object):    
  """
  Images  are  thresholded  at  a  given  value  and  only  voxels at which all images
  exceed the threshold are included.
  """  
  def setThresholdMethodToAbsolute(self):
    """
    Images  are  thresholded  at  a  given  value  and  only  voxels at which all images
    exceed the threshold are included.
    """
    self.method = 'Absolute'
    self.setThreshold( 100 )
    
  def setThresholdMethodToRelative(self):
    """
    Images  are  thresholded  at  a  given  value  and  only  voxels at which all images
    exceed the threshold are included.
    This option allows you to specify the value of the threshold as a proportion of the
    global value.
    """
    self.method = 'Relative'
    self.setThreshold( 0.8 )
    
  def unsetThreshold(self):
    self.method = 'None'
    
  def setThreshold(self, threshold):
    if type(threshold) in [float, int]:
      self.threshold = threshold
    else:
      raise ValueError('Threshold must be a float or an integer, not ' + str(type(threshold)))
    
  def getStringListForBatch( self ):
    batch_list = []
    if self.method == 'None':
      batch_list = ["tm.tm_none = 1;"]
    elif self.method == 'Absolute':
      batch_list = ["tm.tma.athresh = %g;" % self.threshold]
    elif self.method == 'Relative':
      batch_list = ["tm.tmr.rthresh = %g;" % self.threshold]
    else:
      raise ValueError("Unvalid method")
    return batch_list