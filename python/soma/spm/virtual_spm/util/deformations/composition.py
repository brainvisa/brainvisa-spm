# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
from soma.spm.spm_batch_maker_utils import convertlistToSPMString, convertNumpyArrayToSPMString


import numpy  

class Composition(object):
  """
  Deformation  fields  can be thought of as mappings. These can be combined by the operation of
  "composition",  which  is  usually  denoted  by a circle "o". Suppose x:A->B and y:B->C are two
  mappings,  where  A,  B  and  C  refer to domains in 3 dimensions. Each element a in A points to
  element x(a) in B. This in turn points to element y(x(a)) in C, so we have a mapping from A to C.
  The  composition of these mappings is denoted by yox:A->C. Compositions can be combined in
  an associative way, such that zo(yox) = (zoy)ox.
  In  this  utility,  the left-to-right order of the compositions is from top to bottom (note that the
  rightmost  deformation  would  actually  be applied first). i.e. ...((first o second) o third)...o last.
  The  resulting  deformation  field  will  have the same domain as the first deformation specified,
  and will map to voxels in the codomain of the last specified deformation field.
  """
  def getStringListForBatch( self ):
    batch_list = []
    for deformation_index, deformation in enumerate(self):
      batch_list.extend(addBatchKeyWordInEachItem("comp{%s}" % (deformation_index+1), deformation.getStringListForBatch()))
    return batch_list
  
  def getFirstDeformationPath(self):
    """
    This method is used to find output directory if "Source directory (deformation)" options used
    """
    if self:
      return self[0].getInputReferencePath()
    else:
      raise ValueError("No composition found")
#===============================================================================
# 
#===============================================================================
class MatFileImported(object):
  """
  Spatial  normalisation,  and  the unified segmentation model of SPM5 save a parameterisation of
  deformation  fields.  These consist of a combination of an affine transform, and nonlinear warps
  that  are  parameterised  by a linear combination of cosine transform basis functions.  These are
  saved in *_sn.mat files, which can be converted to deformation fields.
  """
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setParameterFile(self, parameter_file_path):
    """
    Specify the _sn.mat to be used.
    """
    self.parameter_file_path = parameter_file_path
    
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setVoxelSize(self, voxel_size_list):
    """
    Specify the voxel sizes of the deformation field to be produced. Non-finite values will default to
    the voxel sizes of the template imagethat was originally used to estimate the deformation.
    Evaluated statements are entered.
    """
    if len(voxel_size_list) == 3:
      self.voxel_size = voxel_size_list
    else:
      raise ValueError("voxel_size_list must have 3 items [x, y, z]")
    
  @checkIfArgumentTypeIsAllowed(numpy.ndarray, 1)
  def setBoundingBox(self, numpy_array):
    """
    Specify  the bounding box of the deformation field to be produced. Non-finite values will default
    to the bounding box of the template imagethat was originally used to estimate the deformation.
    """
    if numpy_array.shape == (2, 3):
      self.bounding_box = numpy_array
    else:
      raise ValueError("An 2-by-3 array must be entered")
    
  def getStringListForBatch( self ):
    if self.parameter_file_path is not None:
      batch_list = []
      batch_list.append("sn2def.matname = {'%s'};" %self.parameter_file_path)
      batch_list.append("sn2def.vox = %s;" %convertlistToSPMString(self.voxel_size))
      batch_list.append("sn2def.bb = %s;" %convertNumpyArrayToSPMString(self.bounding_box))
      return batch_list
    else:
      raise ValueError("parameter file path is required")
    
  def getInputReferencePath(self):
    """
    This method is used to find output directory if "Source directory (deformation)" options used
    """
    if self.parameter_file_path is not None:
      return self.parameter_file_path
    else:
      raise ValueError("parameter file path is required")
#===============================================================================
# 
#===============================================================================
class DartelFlow(object):
  """
  Imported DARTEL flow field.
  """
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setFlowFieldPath(self, flow_field_path):
    """
    The  flow field stores the deformation information. The same field can be used for both forward
    or backward deformations (or even, in principle, half way or exaggerated deformations).
    """
    self.flow_field_path = flow_field_path
    
  def setFlowDirectionToBackward(self):
    """
    The  direction  of  the  DARTEL  flow.    Note  that  a backward transform will warp an individual
    subject's  to match the template (ie maps from template to individual). A forward transform will
    warp the template image to the individual.
    """
    self.flow_direction = [1, 0]
    
  def setFlowDirectionToForward(self):
    """
    The  direction  of  the  DARTEL  flow.    Note  that  a backward transform will warp an individual
    subject's  to match the template (ie maps from template to individual). A forward transform will
    warp the template image to the individual.
    """
    self.flow_direction = [0, 1]
    
  def setTimeStepTo1(self):
    """
    The  number  of  time  points  used  for  solving the partial differential equations.  A single time
    point   would   be   equivalent   to   a   small  deformation  model.  Smaller  values  allow  faster
    computations,  but  are  less  accurate  in  terms  of  inverse  consistency  and may result in the
    """
    self.time_step = 0
    
  def setTimeStepTo2(self):
    """
    The  number  of  time  points  used  for  solving the partial differential equations.  A single time
    point   would   be   equivalent   to   a   small  deformation  model.  Smaller  values  allow  faster
    computations,  but  are  less  accurate  in  terms  of  inverse  consistency  and may result in the
    """
    self.time_step = 1
    
  def setTimeStepTo4(self):
    """
    The  number  of  time  points  used  for  solving the partial differential equations.  A single time
    point   would   be   equivalent   to   a   small  deformation  model.  Smaller  values  allow  faster
    computations,  but  are  less  accurate  in  terms  of  inverse  consistency  and may result in the
    """
    self.time_step = 2
    
  def setTimeStepTo8(self):
    """
    The  number  of  time  points  used  for  solving the partial differential equations.  A single time
    point   would   be   equivalent   to   a   small  deformation  model.  Smaller  values  allow  faster
    computations,  but  are  less  accurate  in  terms  of  inverse  consistency  and may result in the
    """
    self.time_step = 3
    
  def setTimeStepTo16(self):
    """
    The  number  of  time  points  used  for  solving the partial differential equations.  A single time
    point   would   be   equivalent   to   a   small  deformation  model.  Smaller  values  allow  faster
    computations,  but  are  less  accurate  in  terms  of  inverse  consistency  and may result in the
    """
    self.time_step = 4
    
  def setTimeStepTo32(self):
    """
    The  number  of  time  points  used  for  solving the partial differential equations.  A single time
    point   would   be   equivalent   to   a   small  deformation  model.  Smaller  values  allow  faster
    computations,  but  are  less  accurate  in  terms  of  inverse  consistency  and may result in the
    """
    self.time_step = 5
    
  def setTimeStepTo64(self):
    """
    The  number  of  time  points  used  for  solving the partial differential equations.  A single time
    point   would   be   equivalent   to   a   small  deformation  model.  Smaller  values  allow  faster
    computations,  but  are  less  accurate  in  terms  of  inverse  consistency  and may result in the
    """
    self.time_step = 6
    
  def setTimeStepTo128(self):
    """
    The  number  of  time  points  used  for  solving the partial differential equations.  A single time
    point   would   be   equivalent   to   a   small  deformation  model.  Smaller  values  allow  faster
    computations,  but  are  less  accurate  in  terms  of  inverse  consistency  and may result in the
    """
    self.time_step = 7
    
  def setTimeStepTo256(self):
    """
    The  number  of  time  points  used  for  solving the partial differential equations.  A single time
    point   would   be   equivalent   to   a   small  deformation  model.  Smaller  values  allow  faster
    computations,  but  are  less  accurate  in  terms  of  inverse  consistency  and may result in the
    """
    self.time_step = 8
    
  def setTimeStepTo512(self):
    """
    The  number  of  time  points  used  for  solving the partial differential equations.  A single time
    point   would   be   equivalent   to   a   small  deformation  model.  Smaller  values  allow  faster
    computations,  but  are  less  accurate  in  terms  of  inverse  consistency  and may result in the
    """
    self.time_step = 9
    
  def getStringListForBatch( self ):
    if self.flow_field_path is not None:
      batch_list = []
      batch_list.append("dartel.flowfield = {'%s'};" %self.flow_field_path)
      batch_list.append("dartel.times = %s;" %convertlistToSPMString(self.flow_direction))
      batch_list.append("dartel.K = %s;" %self.time_step)
      return batch_list
    else:
      raise ValueError("flow field path is required")
    
  def getInputReferencePath(self):
    """
    This method is used to find output directory if "Source directory (deformation)" options used
    """
    if self.flow_field_path is not None:
      return self.flow_field_path
    else:
      raise ValueError("flow field path is required")
#===============================================================================
# 
#===============================================================================
class DeformationField(object):
  """
  Deformations  can  be  thought  of  as  vector fields. These can be represented by three-volume
  images.
  """
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setDeformationFieldPath(self, deformation_field_path):
    """
    The  flow field stores the deformation information. The same field can be used for both forward
    or backward deformations (or even, in principle, half way or exaggerated deformations).
    """
    self.deformation_field_path = deformation_field_path
    
  def getStringListForBatch( self ):
    if self.deformation_field_path is not None:
      batch_list = []
      batch_list.append("def = {'%s'};" %self.deformation_field_path)
      return batch_list
    else:
      raise ValueError("deformation field path is required")
    
  def getInputReferencePath(self):
    """
    This method is used to find output directory if "Source directory (deformation)" options used
    """
    if self.deformation_field_path is not None:
      return self.deformation_field_path
    else:
      raise ValueError("deformation field path is required")
#===============================================================================
# 
#===============================================================================
class IdentityFromImage(object):
  """
  This  option  generates  an identity transform, but this can be useful for changing
  the  dimensions  of  the resulting deformation (and any images that are generated
  from it).  Dimensions, orientation etc are derived from an image.
  """
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setImageToBaseIdOn(self, reference_image_path):
    """
    Specify the image file on which to base the dimensions, orientation etc.
    """
    self.reference_image_path = reference_image_path
    
  def getStringListForBatch( self ):
    if self.reference_image_path is not None:
      batch_list = []
      batch_list.append("id.space = {'%s,1'};" %self.reference_image_path)
      return batch_list
    else:
      raise ValueError("reference image path is required")
    
  def getInputReferencePath(self):
    """
    This method is used to find output directory if "Source directory (deformation)" options used
    """
    if self.reference_image_path is not None:
      return self.reference_image_path
    else:
      raise ValueError("reference image path is required")
#===============================================================================
# 
#===============================================================================
class Identity(object):
  """
  This is a utility for working with deformation fields. They can be loaded, inverted,
  combined etc, and the results either saved to disk, or applied to some image.
  """
  @checkIfArgumentTypeIsAllowed(numpy.ndarray, 1)
  def setVoxelSize(self, voxel_size_list):
    if len(voxel_size_list) == 3:
      self.voxel_size = voxel_size_list
    else:
      raise ValueError("voxel_size_list must have 3 items [x, y, z]")
    
  @checkIfArgumentTypeIsAllowed(numpy.ndarray, 1)
  def setBoundingBox(self, numpy_array):
    if numpy_array.shape == (2, 3):
      self.bounding_box = numpy_array
    else:
      raise ValueError("An 2-by-3 array must be entered")
    
  def getStringListForBatch( self ):
    if not None in [self.voxel_size, self.bounding_box]:
      batch_list = []
      batch_list.append("idbbvox.vox = %s;" %convertlistToSPMString(self.voxel_size))
      batch_list.append("idbbvox.bb = %s;" %convertNumpyArrayToSPMString(self.bounding_box))
      return batch_list
    else:
      raise ValueError("voxel size and bounding box are mandatory")
    
  def getInputReferencePath(self):
    """
    This method is used to find output directory if "Source directory (deformation)" options used
    """
    raise ValueError("No reference image path for Identity Deformation")
#===============================================================================
# 
#===============================================================================
class Inverse(object):
  """
  Creates  the  inverse  of  a  deformation  field.  Deformations  are  assumed to be
  one-to-one,  in  which  case they have a unique inverse.  If y':A->B is the inverse
  of y:B->A, then y' o y = y o y' = Id, where Id is the identity transform.
  """

  def setDeformationComposition(self, composition):
    """
    Deformation  fields  can be thought of as mappings. These can be combined by the operation of
    "composition",  which  is  usually  denoted  by a circle "o". Suppose x:A->B and y:B->C are two
    mappings,  where  A,  B  and  C  refer to domains in 3 dimensions. Each element a in A points to
    element x(a) in B. This in turn points to element y(x(a)) in C, so we have a mapping from A to C.
    The  composition of these mappings is denoted by yox:A->C. Compositions can be combined in
    an associative way, such that zo(yox) = (zoy)ox.
    In  this  utility,  the left-to-right order of the compositions is from top to bottom (note that the
    rightmost  deformation  would  actually  be applied first). i.e. ...((first o second) o third)...o last.
    The  resulting  deformation  field  will  have the same domain as the first deformation specified,
    and will map to voxels in the codomain of the last specified deformation field.
    """
    self.composition = composition
      
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setImageToBaseInverseOn(self, image_path):
    """
    Specify the image file on which to base the dimensions, orientation etc.
    """
    self.reference_image_path = image_path
    
  def getStringListForBatch( self ):
    if not None in [self.composition, self.reference_image_path]:
      batch_list = []
      batch_list.extend(addBatchKeyWordInEachItem("inv", self.composition.getStringListForBatch()))
      batch_list.append("inv.space = {'%s,1'};" %self.reference_image_path)
      return batch_list
    else:
      raise ValueError("voxel size and bounding box are mandatory")
    
  def getInputReferencePath(self):
    """
    This method is used to find output directory if "Source directory (deformation)" options used
    """
    return self.composition.getInputReferencePath()
