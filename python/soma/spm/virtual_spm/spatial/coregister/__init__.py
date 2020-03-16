 # -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem, moveSPMPath
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode

from soma.spm.virtual_spm.spatial.coregister.estimation_options import EstimationOptions
from soma.spm.virtual_spm.spatial.coregister.reslice_options import ResliceOptions
from six.moves import zip

class Coregister(object):
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setReferenceVolumePath(self, reference_volume_path):
    """
    This is the image that is assumed to remain stationary (sometimes known as the target or
    template image), while the source image is moved to match it.
    """
    self.reference_volume_path = reference_volume_path
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setSourceVolumePath(self, source_volume_path):
    """
    This is the image that is jiggled about to best match the reference.
    """
    self.source_volume_path = source_volume_path
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def addOtherVolumePath(self, other_volume_path):
    """
    These are any images that need to remain in alignment with the source image.
    """
    if self.other_volume_path_list is not None:
      self.other_volume_path_list.append(other_volume_path)
    else:
      self.other_volume_path_list = [other_volume_path]
      
  @checkIfArgumentTypeIsAllowed(list, 1)  
  def setOtherVolumesPathList(self, other_volume_path_list):
    """
    These are any images that need to remain in alignment with the source image.
    """
    self.other_volume_path_list = []
    for other_volume_path in other_volume_path_list:
      self.addOtherVolumePath(other_volume_path)
#===============================================================================
# 
#===============================================================================
class EstimateAndReslice(Coregister):
  """
  The  registration  method  used  here  is  based  on  work  by  Collignon  et  al. The original
  interpolation   method   described  in  this  paper  has  been  changed  in  order  to  give  a
  smoother cost function.  The images are also smoothed slightly, as is the histogram.  This
  is all in order to make the cost function as smooth as possible, to give faster convergence
  and less chance of local minima.
  At  the  end  of coregistration, the voxel-to-voxel affine transformation matrix is displayed,
  along   with  the  histograms  for  the  images  in  the  original  orientations,  and  the  final
  orientations.  The registered images are displayed at the bottom.
  Registration parameters are stored in the headers of the "source" and the "other" images.
  These  images  are  also  resliced  to match the source image voxel-for-voxel. The resliced
  images are named the same as the originals except that they are prefixed by 'r'.
  """
  @checkIfArgumentTypeIsAllowed(EstimationOptions, 1)  
  def replaceEstimationOptions(self, estimation_options):
    del self.estimation_options
    self.estimation_options = estimation_options
    
  @checkIfArgumentTypeIsAllowed(ResliceOptions, 1)  
  def replaceResliceOptions(self, reslice_options):
    del self.reslice_options
    self.reslice_options = reslice_options
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setSourceWarpedPath(self, output_path):
    self.source_warped_volume_path = output_path
    
  @checkIfArgumentTypeIsAllowed(list, 1)  
  def setOtherVolumesWarpedPathList(self, output_path_list):
    self.other_warped_volume_path_list = output_path_list
    
  def getStringListForBatch(self):
    if not None in [self.reference_volume_path, self.source_volume_path]: 
      other_volume_path_list_for_batch = [] 
      if self.other_volume_path_list is not None:
        for other_volume_path in self.other_volume_path_list:
          other_volume_path_list_for_batch.append("'%s,1'" % other_volume_path)
        other_volume_path_for_batch = '\n'.join(other_volume_path_list_for_batch)
      else:
        other_volume_path_for_batch = """''"""
      batch_list = []
      batch_list.append("spm.spatial.coreg.estwrite.ref = {'%s,1'};" % self.reference_volume_path)
      batch_list.append("spm.spatial.coreg.estwrite.source = {'%s,1'};" % self.source_volume_path)
      batch_list.append("spm.spatial.coreg.estwrite.other = {%s};" % other_volume_path_for_batch)
      batch_list.extend(addBatchKeyWordInEachItem("spm.spatial.coreg.estwrite", self.estimation_options.getStringListForBatch()))
      batch_list.extend(addBatchKeyWordInEachItem("spm.spatial.coreg.estwrite", self.reslice_options.getStringListForBatch()))
      return batch_list
    else:
      raise ValueError('Reference and source volumes are mandatory')
  
  def _moveSPMDefaultPathsIfNeeded(self):
    filename_prefix = self.reslice_options.getCurrentFilenamePrefix()
    if self.source_warped_volume_path is not None:
      moveSPMPath(self.source_volume_path, 
                  self.source_warped_volume_path,
                  prefix=filename_prefix)
    if not None in [self.other_volume_path_list, self.other_warped_volume_path_list]:
      if len(self.other_volume_path_list) == len(self.other_warped_volume_path_list):
        for other_path, warped_path in zip(self.other_volume_path_list, 
                                           self.other_warped_volume_path_list):
          moveSPMPath(other_path, 
                      warped_path,
                      prefix=filename_prefix)
      else:
        raise ValueError("output_path_list has not the same length than other_volume_path_list")
    else:
      pass#No others paths
        
  
#===============================================================================
# 
#===============================================================================
class Estimate(Coregister):
  """
  The   registration  method  used  here  is  based  on  work  by  Collignon  et  al.  The  original
  interpolation  method  described  in  this paper has been changed in order to give a smoother
  cost  function.    The  images  are  also  smoothed  slightly, as is the histogram.  This is all in
  order  to  make  the cost function as smooth as possible, to give faster convergence and less
  chance of local minima.
  Registration parameters are stored in the headers of the "source" and the "other" images.
  """
  @checkIfArgumentTypeIsAllowed(EstimationOptions, 1)  
  def replaceEstimationOptions(self, estimation_options):
    del self.estimation_options
    self.estimation_options = estimation_options
    
  def getStringListForBatch(self):
    if not None in [self.reference_volume_path, self.source_volume_path]: 
      other_volume_path_list_for_batch = [] 
      if self.other_volume_path_list is not None:
        for other_volume_path in self.other_volume_path_list:
          other_volume_path_list_for_batch.append("'%s,1'" % other_volume_path)
        other_volume_path_for_batch = '\n'.join(other_volume_path_list_for_batch)
      else:
        other_volume_path_for_batch = """''"""
      batch_list = []
      batch_list.append("spm.spatial.coreg.estimate.ref = {'%s,1'};" % self.reference_volume_path)
      batch_list.append("spm.spatial.coreg.estimate.source = {'%s,1'};" % self.source_volume_path)
      batch_list.append("spm.spatial.coreg.estimate.other = {%s};" % other_volume_path_for_batch)
      batch_list.extend(addBatchKeyWordInEachItem("spm.spatial.coreg.estimate", self.estimation_options.getStringListForBatch()))
      return batch_list
    else:
      raise ValueError('Reference and source volumes are mandatory')