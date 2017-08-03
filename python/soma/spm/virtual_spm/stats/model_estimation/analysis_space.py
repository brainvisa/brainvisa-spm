# -*- coding: utf-8 -*-
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode

class AnalysisSpace():
  """
  Because estimation can be time consuming options are provided to analyse selected slices or clusters rather than the whole volume.
  """
  def setSlicesBlockType(self):
    self.block_type = 'Slices'

  def setSubvolumesBlockType(self):
    self.block_type = 'Subvolumes'
#==============================================================================
class AnalysisSpaceVolume(AnalysisSpace):
  """
  A  volume  of  data is analysed in "blocks", which can be a slice or 3D subvolume,
  where  the  extent  of  each  subvolume  is  determined using a graph partitioning
  algorithm. Enter the block type, i.e. "Slices" or "Subvolumes".
  """
  def __init__(self):
    AnalysisSpace.__init__(self)
  
  def getStringListForBatch( self ):
    batch_list = ["space.volume.block_type = '%s';" % self.block_type]
    return batch_list
#==============================================================================
class AnalysisSpaceSlices(AnalysisSpace):
  """
  Enter  Slice  Numbers.  This  can be a single slice or multiple slices. If you select a
  single  slice  or  only  a  few slices you must be aware of the interpolation options
  when,  after  estimation, displaying the estimated images eg. images of contrasts
  or  AR  maps. The default interpolation option may need to be changed to nearest
  neighbour (NN) (see bottom right hand of graphics window) for you slice maps to
  be visible.
  """
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setSliceNumberList(self, slice_number_list):
    self.slice_number_list = slice_number_list
  
  def getStringListForBatch( self ):
    if self.slice_number_list is not None:
      if len(self.slice_number_list) == 1:
        batch_list = ["space.slices.numbers = %g;" % self.slice_number_list[0]]
      else:
        slice_number_list_str = [str(coeff) for coeff in self.slice_number_list]
        slice_number_str = '\n'.join(slice_number_list_str)
        batch_list = ["space.slices.numbers = [%s];" % slice_number_str]
      batch_list.append("space.slices.block_type = '%s';" % self.block_type)
      return batch_list
    else:
      raise ValueError('Unvalid Analysis space slices, Slice number not found')
#==============================================================================
class AnalysisSpaceClusters(AnalysisSpace):
  """
  Because  estimation  can  be  time  consuming  an  option  is  provided to analyse
  selected clusters rather than the whole volume.
  """
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setClusterMask(self, cluster_mask_path):
    self.cluster_mask_path = cluster_mask_path

  def clearClusterMask(self):
    self.cluster_mask_path = ''
  
  def getStringListForBatch( self ):
    if self.cluster_mask_path == '':
      batch_list = ["space.clusters.mask = {''};"]
    else:
      batch_list = ["space.clusters.mask = {'%s,1'};" % self.cluster_mask_path]
    batch_list.append("space.slices.block_type = '%s';" % self.block_type)
    return batch_list
#==============================================================================
