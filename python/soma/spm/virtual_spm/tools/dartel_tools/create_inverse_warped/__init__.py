# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.spm_batch_maker_utils import moveFileAndCreateFoldersIfNeeded,\
  convertPathListToSPMBatchString

import os
from six.moves import zip

class CreateInverseWarped(object):
  """
  Create   inverse   normalised   versions   of   some  image(s).  The  image  that  is
  inverse-normalised  should  be  in  alignment with the template (generated during
  the  warping  procedure).  Note  that the results have the same dimensions as the
  ``flow   fields'',   but   are   mapped   to   the   original   images   via   the  affine
  transformations in their headers.
  """
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setFlowFieldPathList(self, flow_field_path_list):
    """
    The  flow  fields  store  the deformation information. The same fields can be used
    for  both  forward  or  backward  deformations  (or  even, in principle, half way or
    exaggerated deformations).
    """
    self.flow_field_list = flow_field_path_list
    
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setImagePathList(self, image_path_list):
    """
    Select  the  image(s) to be inverse normalised.  These should be in alignment with
    the template image generated by the warping procedure.
    """
    self.image_path_list = image_path_list

  @checkIfArgumentTypeIsAllowed(int, 1)
  def setTimeSteps(self, time_steps):
    """
    The  number  of  time  points  used  for solving the partial differential equations. 
    Note  that  Jacobian determinants are not very accurate for very small numbers of
    time steps (less than about 16).
    """
    if time_steps in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]:
      #WARNING : For SPM batch, it is the index in this list to write! (but i don't know why SPM do this)
      self.time_steps = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512].index(time_steps)
    else:
      raise ValueError("Unvalid time steps")
    
  def setInterpolationToNearestNeighbour(self):
    """
    The  method  by which the images are sampled when being written in a different space. (Note that Inf or NaN values are treated as zero,
    rather than as missing data)
        Nearest Neighbour:
        - Fastest, but not normally recommended.
    """
    self.interpolation = 0
    
  def setInterpolationToTrilinear(self):
    """
    The  method  by which the images are sampled when being written in a different space. (Note that Inf or NaN values are treated as zero,
    rather than as missing data)
        Trilinear Interpolation:
        - OK for PET, realigned fMRI, or segmentations
    """
    self.interpolation = 1
    
  def setInterpolationTo2ndDegreeBSpline(self):
    """
    The  method  by which the images are sampled when being written in a different space. (Note that Inf or NaN values are treated as zero,
    rather than as missing data)
        B-spline Interpolation:
          - Better  quality  (but  slower) interpolation, especially with higher degree splines. Can produce values outside the original range (e.g.
            small negative values from an originally all positive image).
    """
    self.interpolation = 2
    
  def setInterpolationTo3dDegreeBSpline(self):
    """
    The  method  by which the images are sampled when being written in a different space. (Note that Inf or NaN values are treated as zero,
    rather than as missing data)
        B-spline Interpolation:
          - Better  quality  (but  slower) interpolation, especially with higher degree splines. Can produce values outside the original range (e.g.
            small negative values from an originally all positive image).
    """
    self.interpolation = 3
    
  def setInterpolationTo4thDegreeBSpline(self):
    """
    The  method  by which the images are sampled when being written in a different space. (Note that Inf or NaN values are treated as zero,
    rather than as missing data)
        B-spline Interpolation:
          - Better  quality  (but  slower) interpolation, especially with higher degree splines. Can produce values outside the original range (e.g.
            small negative values from an originally all positive image).
    """
    self.interpolation = 4
    
  def setInterpolationTo5thDegreeBSpline(self):
    """
    The  method  by which the images are sampled when being written in a different space. (Note that Inf or NaN values are treated as zero,
    rather than as missing data)
        B-spline Interpolation:
          - Better  quality  (but  slower) interpolation, especially with higher degree splines. Can produce values outside the original range (e.g.
            small negative values from an originally all positive image).
    """
    self.interpolation = 5
    
  def setInterpolationTo6thDegreeBSpline(self):
    """
    The  method  by which the images are sampled when being written in a different space. (Note that Inf or NaN values are treated as zero,
    rather than as missing data)
        B-spline Interpolation:
          - Better  quality  (but  slower) interpolation, especially with higher degree splines. Can produce values outside the original range (e.g.
            small negative values from an originally all positive image).
    """
    self.interpolation = 6
    
  def setInterpolationTo7thDegreeBSpline(self):
    """
    The  method  by which the images are sampled when being written in a different space. (Note that Inf or NaN values are treated as zero,
    rather than as missing data)
        B-spline Interpolation:
          - Better  quality  (but  slower) interpolation, especially with higher degree splines. Can produce values outside the original range (e.g.
            small negative values from an originally all positive image).
    """
    self.interpolation = 7
    
  def setOutputWarpedPathList(self, output_warped_path_list):
    self.output_warped_path_list = output_warped_path_list

  def getStringListForBatch( self ):
    if self.image_path_list and self.flow_field_list:
      batch_list = []
      batch_list.append("spm.tools.dartel.crt_iwarped.flowfields = {%s};" % convertPathListToSPMBatchString(self.flow_field_list,
                                                                                                          add_dimension=False))
      batch_list.append("spm.tools.dartel.crt_iwarped.images = {%s};" % convertPathListToSPMBatchString(self.image_path_list,
                                                                                                          add_dimension=False))
      batch_list.append("spm.tools.dartel.crt_iwarped.K = %i;" % self.time_steps)
      batch_list.append("spm.tools.dartel.crt_iwarped.interp = %i;" % self.interpolation)
      return batch_list
    else:
      raise ValueError('images_list_list and/or flow_field_list not found')
    
  def _moveSPMDefaultPathsIfNeeded(self):
    #images warped path : <flow_field dir>/w<image_basename>
    if self.output_warped_path_list is not None:
      if len(self.image_path_list) == len(self.output_warped_path_list):
        for image_path, output_warped_path, flow_field in zip(self.image_path_list, self.output_warped_path_list, self.flow_field_list):
          flow_field_dir = os.path.dirname(flow_field)
          flow_field_basename = os.path.basename(flow_field)
          image_basename = os.path.basename(image_path).split('.')[0]
          output_basename = "w" + image_basename + '_' + flow_field_basename
          spm_default_output_path = os.path.join(flow_field_dir, output_basename)
          moveFileAndCreateFoldersIfNeeded(spm_default_output_path, output_warped_path)
      else:
        raise ValueError("images_list length do not coincide with output_warped_path_list length")
        
    
