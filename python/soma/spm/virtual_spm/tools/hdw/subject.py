 # -*- coding: utf-8 -*-
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsStrOrUnicode
from soma.spm.spm_batch_maker_utils import moveSPMPath

class Subject():
  """
  Two  images  of  the  same  subject, which are to be registered together.  Prior to
  nonlinear  high-dimensional warping, the images should be rigidly registered with
  each other.
  """
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setReferenceImage(self, image_path):
    """
    This is the reference image, which remains stationary.
    """
    self.reference_image_path = image_path
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setMovedImage(self, image_path):
    """
    This is the moved image, which is warped to match the reference.
    """
    self.moved_image_path = image_path
    
  def setOutputDeformationFieldPath(self, output_deformation_field_path):
    self.output_deformation_field_path = output_deformation_field_path
    
  def setOutputJacobianDeterminantPath(self, output_jacobian_determinant_path):
    self.output_jacobian_determinant_path = output_jacobian_determinant_path
    
  def getStringListForBatch(self):
    if not None in [self.reference_image_path, self.moved_image_path]:
      batch_list = []
      batch_list.append("ref = {'%s,1'};" % self.reference_image_path)
      batch_list.append("mov = {'%s,1'};" % self.moved_image_path)
      return batch_list
    else:
      raise ValueError("source_image_path is mandatory")
    
  def movePathsIfNeeded(self):
    if self.output_deformation_field_path is not None:
      moveSPMPath(self.moved_image_path,
                  self.output_deformation_field_path,
                  prefix="y_")
    if self.output_jacobian_determinant_path is not None:
      moveSPMPath(self.moved_image_path,
                  self.output_jacobian_determinant_path,
                  prefix="jy_")