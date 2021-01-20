# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem, moveSPMPath, convertlistToSPMString
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
class MatterWritingOptions(object):
  """
  This routine produces spatial normalisation parameters (*_seg8.mat files) by default.
  In  addition,  it  also produces files that can be used for doing inverse normalisation. If you
  have  an  image  of  regions  defined in the standard space, then the inverse deformations
  have  an  image  of  regions  defined in the standard space, then the inverse deformations
  can  be  used  to  warp  these regions so that it approximately overlay your image. To use
  this facility, the bounding-box and voxel sizes should be set to non-finite values (e.g. [NaN
  NaN  NaN]  for  the  voxel  sizes,  and ones(2,3)*NaN for the bounding box. This would be
  done  by  the  spatial normalisation module, which allows you to select a set of parameters
  that describe the nonlinear warps, and the images that they should be applied to...
  """
  def __init__(self, dartel_normalization):
    self.dartel_normalization = dartel_normalization

    self._batch_prefix = None
    self.native = 0
    self.normalized = 0
    self.modulated = 0
    self.dartel = 0

    self.native_prefix = None
    self.normalized_prefix = None
    self.modulated_affine_and_non_linear_prefix = None
    self.modulated_non_linear_prefix = None
    self.dartel_rigid_prefix = None
    self.dartel_affine_prefix = None
    self.dartel_affine_suffix = None

    self.native_path = None
    self.normalized_path = None
    self.modulated_affine_and_non_linear_path = None
    self.modulated_non_linear_path = None
    self.dartel_rigid_path = None
    self.dartel_affine_path = None

  def unsetNative(self):
    """
    The  native  space  option  allows  you  to  produce  a  tissue  class  image  (p*)  that  is  in
    alignment  with  the  original.  It  can  also  be  used for ''importing'' into a form that can be
    used with the DARTEL toolbox (rp*).
    """
    self.native = 0

  def setNative(self):
    """
    The  native  space  option  allows  you  to  produce  a  tissue  class  image  (p*)  that  is  in
    alignment  with  the  original.  It  can  also  be  used for ''importing'' into a form that can be
    used with the DARTEL toolbox (rp*).
    """
    self.native = 1

  def unsetNormalized(self):
    """
    Write image in normalized space.
    """
    self.normalized = 0

  def setNormalized(self):
    """
    Write image in normalized space.
    """
    self.normalized = 1

  def unsetModulation(self):
    """
    'Modulation''  is to compensate for the effect of spatial normalisation. Spatial normalisation
    causes  volume  changes  due  to  affine  transformation  (global  scaling)  and  non-linear
    warping  (local  volume  change).  The  SPM  default  is  to adjust spatially normalised grey
    matter  (or  other  tissue  class)  by using both terms and the resulting modulated images
    are  preserved  for  the  total  amount of grey matter. Thus, modulated images reflect the
    grey matter volumes before spatial normalisation. However, the user is often interested in
    removing  the  confound  of  different  brain  sizes and there are many ways to apply this
    correction.  We  can  use  the  total  amount  of  GM,  GM+WM, GM+WM+CSF, or manual
    estimated  total intracranial volume (TIV). Theses parameters can be modeled as nuisance
    parameters  (additive  effects)  in  an  AnCova  model  or  used  to  globally scale the data
    (multiplicative effects):
    """
    self.modulated = 0

  def setModulationToAffineAndNonLinear(self):
    """
    'Modulation''  is to compensate for the effect of spatial normalisation. Spatial normalisation
    causes  volume  changes  due  to  affine  transformation  (global  scaling)  and  non-linear
    warping  (local  volume  change).  The  SPM  default  is  to adjust spatially normalised grey
    matter  (or  other  tissue  class)  by using both terms and the resulting modulated images
    are  preserved  for  the  total  amount of grey matter. Thus, modulated images reflect the
    grey matter volumes before spatial normalisation. However, the user is often interested in
    removing  the  confound  of  different  brain  sizes and there are many ways to apply this
    correction.  We  can  use  the  total  amount  of  GM,  GM+WM, GM+WM+CSF, or manual
    estimated  total intracranial volume (TIV). Theses parameters can be modeled as nuisance
    parameters  (additive  effects)  in  an  AnCova  model  or  used  to  globally scale the data
    (multiplicative effects):
    """
    self.modulated = 1

  def setModulationToNonLinear(self):
    """
    'Modulation''  is to compensate for the effect of spatial normalisation. Spatial normalisation
    causes  volume  changes  due  to  affine  transformation  (global  scaling)  and  non-linear
    warping  (local  volume  change).  The  SPM  default  is  to adjust spatially normalised grey
    matter  (or  other  tissue  class)  by using both terms and the resulting modulated images
    are  preserved  for  the  total  amount of grey matter. Thus, modulated images reflect the
    grey matter volumes before spatial normalisation. However, the user is often interested in
    removing  the  confound  of  different  brain  sizes and there are many ways to apply this
    correction.  We  can  use  the  total  amount  of  GM,  GM+WM, GM+WM+CSF, or manual
    estimated  total intracranial volume (TIV). Theses parameters can be modeled as nuisance
    parameters  (additive  effects)  in  an  AnCova  model  or  used  to  globally scale the data
    (multiplicative effects):
    """
    self.modulated = 2

  def unsetDartelExport(self):
    """
    This  option  is  to export data into a form that can be used with DARTEL.The SPM8 default
    is   to   only   apply   rigid  body  transformation.  An  additional  option  is  to  apply  affine
    transformation.
    """
    self.dartel = 0

  def setDartelExportToRigid(self):
    """
    This  option  is  to export data into a form that can be used with DARTEL.The SPM8 default
    is   to   only   apply   rigid  body  transformation.  An  additional  option  is  to  apply  affine
    transformation.
    """
    self.dartel = 1

  def setDartelExportToAffine(self):
    """
    This  option  is  to export data into a form that can be used with DARTEL.The SPM8 default
    is   to   only   apply   rigid  body  transformation.  An  additional  option  is  to  apply  affine
    transformation.
    """
    self.dartel = 2

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setNativePath(self, native_path):
    self.native_path = native_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setNormalizedPath(self, normalized_path):
    self.normalized_path = normalized_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setModulatedAffineAndNonLinearPath(self, modulated_affine_and_non_linear_path):
    self.modulated_affine_and_non_linear_path = modulated_affine_and_non_linear_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setModulatedNonLinearPath(self, modulated_non_linear_path):
    self.modulated_non_linear_path = modulated_non_linear_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setDartelRigidPath(self, dartel_rigid_path):
    self.dartel_rigid_path = dartel_rigid_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setDartelAffinePath(self, dartel_affine_path):
    self.dartel_affine_path = dartel_affine_path

  def getStringListForBatch(self):
    if self._batch_prefix is not None:
      batch_list = []
      batch_list.append("native = %s;" % self.native)
      batch_list.append("warped = %s;" % self.normalized)
      batch_list.append("modulated = %s;" % self.modulated)
      batch_list.append("dartel = %s;" % self.dartel)
      return addBatchKeyWordInEachItem(self._batch_prefix, batch_list)
    else:
      raise Exception("Do not use MatterWritingOptions class but one of its daughter")

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def moveSPMDefaultPathsIfNeeded(self, volume_reference_path):
    if self.native_path is not None:
      moveSPMPath(volume_reference_path,
                  self.native_path,
                  prefix=self.native_prefix)
    if self.normalized_path is not None:
      moveSPMPath(volume_reference_path,
                  self.normalized_path,
                  prefix=self.normalized_prefix)
    if self.modulated_affine_and_non_linear_path is not None:
      moveSPMPath(volume_reference_path,
                  self.modulated_affine_and_non_linear_path,
                  prefix=self.modulated_affine_and_non_linear_prefix)
    if self.modulated_non_linear_path is not None:
      moveSPMPath(volume_reference_path,
                  self.modulated_non_linear_path,
                  prefix=self.modulated_non_linear_prefix)
    if self.dartel_rigid_path is not None:
      moveSPMPath(volume_reference_path,
                  self.dartel_rigid_path,
                  prefix=self.dartel_rigid_prefix)
    if self.dartel_affine_path is not None:
      moveSPMPath(volume_reference_path,
                  self.dartel_affine_path,
                  prefix=self.dartel_affine_prefix,
                  suffix=self.dartel_affine_suffix)
    #===========================================================================
    #
    #===========================================================================
class GreyMatterWritingOptions(MatterWritingOptions):
  def __init__(self, dartel_normalization):
    MatterWritingOptions.__init__(self, dartel_normalization)
    self._batch_prefix = "GM"

    self.native_prefix = "p1"
    if dartel_normalization:
      self.normalized_prefix = "wrp1"
      self.modulated_affine_and_non_linear_prefix = "mwrp1"
      self.modulated_non_linear_prefix = "m0wrp1"
    else:
      self.normalized_prefix = "wp1"
      self.modulated_affine_and_non_linear_prefix = "mwp1"
      self.modulated_non_linear_prefix = "m0wp1"
    self.dartel_rigid_prefix = "rp1"
    self.dartel_affine_prefix = prefix="rp1"
    self.dartel_affine_suffix = "_affine"

class WhiteMatterWritingOptions(MatterWritingOptions):
  def __init__(self, dartel_normalization):
    MatterWritingOptions.__init__(self, dartel_normalization)
    self._batch_prefix = "WM"

    self.native_prefix = "p2"
    if dartel_normalization:
      self.normalized_prefix = "wrp2"
      self.modulated_affine_and_non_linear_prefix = "mwrp2"
      self.modulated_non_linear_prefix = "m0wrp2"
    else:
      self.normalized_prefix = "wp2"
      self.modulated_affine_and_non_linear_prefix = "mwp2"
      self.modulated_non_linear_prefix = "m0wp2"
    self.dartel_rigid_prefix = "rp2"
    self.dartel_affine_prefix = prefix="rp2"
    self.dartel_affine_suffix = "_affine"

class CSFMatterWritingOptions(MatterWritingOptions):
  def __init__(self, dartel_normalization):
    MatterWritingOptions.__init__(self, dartel_normalization)
    self._batch_prefix = "CSF"

    self.native_prefix = "p3"
    if dartel_normalization:
      self.normalized_prefix = "wrp3"
      self.modulated_affine_and_non_linear_prefix = "mwrp3"
      self.modulated_non_linear_prefix = "m0wrp3"
    else:
      self.normalized_prefix = "wp3"
      self.modulated_affine_and_non_linear_prefix = "mwp3"
      self.modulated_non_linear_prefix = "m0wp3"
    self.dartel_rigid_prefix = "rp3"
    self.dartel_affine_prefix = prefix="rp3"
    self.dartel_affine_suffix = "_affine"
    #===========================================================================
    #
    #===========================================================================
class BiasCorrectedWritingOptions(object):
  """
  This  is  the  option  to save a bias corrected version of your image. MR images are usually
  corrupted  by a smooth, spatially varying artifact that modulates the intensity of the image
  (bias).  These  artifacts,  although  not  usually a problem for visual inspection, can impede
  automated  processing  of  the  images.  The  bias  corrected  version  should  have  more
  uniform  intensities  within  the different types of tissues and can be saved in native space
  and/or normalised.
  """
  def __init__(self, dartel_normalization):

    self.native = 0
    self.normalized = 1
    self.affine = 0

    self.native_prefix = "m"
    if dartel_normalization:
      self.normalized_prefix = "wmr"
    else:
      self.normalized_prefix = "wm"
    self.affine_prefix = "wm"
    self.affine_suffix = "_affine"

    self.native_path = None
    self.normalized_path = None
    self.affine_path = None

  def unsetNative(self):
    self.native = 0

  def setNative(self):
    self.native = 1

  def unsetNormalized(self):
    self.normalized = 0

  def setNormalized(self):
    self.normalized = 1

  def unsetAffine(self):
    """
    Write image in normalized space, but restricted to affine transformation.
    """
    self.affine = 0

  def setAffine(self):
    """
    Write image in normalized space, but restricted to affine transformation.
    """
    self.affine = 1

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setNativePath(self, native_path):
    self.native_path = native_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setNormalizedPath(self, normalized_path):
    self.normalized_path = normalized_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setAffinePath(self, affine_path):
    self.affine_path = affine_path

  def getStringListForBatch(self):
    batch_list = []
    batch_list.append("bias.native = %s;" % self.native)
    batch_list.append("bias.warped = %s;" % self.normalized)
    batch_list.append("bias.affine = %s;" % self.affine)
    return batch_list

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def moveSPMDefaultPathsIfNeeded(self, volume_reference_path):
    if self.native_path is not None:
      moveSPMPath(volume_reference_path,
                  self.native_path,
                  prefix=self.native_prefix)
    if self.normalized_path is not None:
      moveSPMPath(volume_reference_path,
                  self.normalized_path,
                  prefix=self.normalized_prefix)
    if self.affine_path is not None:
      moveSPMPath(volume_reference_path,
                  self.affine_path,
                  prefix=self.affine_prefix,
                  suffix=self.affine_suffix)
    #===========================================================================
    #
    #===========================================================================
class PVELabelWritingOptions(object):
  """
  This  is  the  option  to  save  a labeled version of your segmentations. Labels are saved as
  Partial Volume Estimation (PVE) values with different mix classes for GM-WM and GM-CSF.
  """
  def __init__(self, dartel_normalization):
    self.native = 0
    self.normalized = 0
    self.dartel = 0

    self.native_prefix = "p0"
    if dartel_normalization:
      self.normalized_prefix = "wrp0"
    else:
      self.normalized_prefix = "wp0"
    self.dartel_rigid_prefix = "rp0"
    self.dartel_affine_prefix = "rp0"
    self.dartel_affine_suffix = "_affine"

    self.native_path = None
    self.normalized_path = None
    self.dartel_rigid_path = None
    self.dartel_affine_path = None

  def unsetNative(self):
    self.native = 0

  def setNative(self):
    self.native = 1

  def unsetNormalized(self):
    self.normalized = 0

  def setNormalized(self):
    self.normalized = 1

  def unsetDartelExport(self):
    self.dartel = 0

  def setDartelExportToRigid(self):
    self.dartel = 1

  def setDartelExportToAffine(self):
    self.dartel = 2

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setNativePath(self, native_path):
    self.native_path = native_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setNormalizedPath(self, normalized_path):
    self.normalized_path = normalized_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setDartelRigidPath(self, dartel_rigid_path):
    self.dartel_rigid_path = dartel_rigid_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setDartelAffinePath(self, dartel_affine_path):
    self.dartel_affine_path = dartel_affine_path

  def getStringListForBatch(self):
    batch_list = []
    batch_list.append("label.native = %s;" % self.native)
    batch_list.append("label.warped = %s;" % self.normalized)
    batch_list.append("label.dartel = %s;" % self.dartel)
    return batch_list

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def moveSPMDefaultPathsIfNeeded(self, volume_reference_path):
    if self.native_path is not None:
      moveSPMPath(volume_reference_path,
                  self.native_path,
                  prefix=self.native_prefix)
    if self.normalized_path is not None:
      moveSPMPath(volume_reference_path,
                  self.normalized_path,
                  prefix=self.normalized_prefix)
    if self.dartel_rigid_path is not None:
      moveSPMPath(volume_reference_path,
                  self.dartel_rigid_path,
                  prefix=self.dartel_rigid_prefix)
    if self.dartel_affine_path is not None:
      moveSPMPath(volume_reference_path,
                  self.dartel_affine_path,
                  prefix=self.dartel_affine_prefix,
                  suffix=self.dartel_affine_suffix)
    #===========================================================================
    #
    #===========================================================================
class WritingOptions(object):
  def __init__(self, dartel_normalization):
    self.dartel_normalization = dartel_normalization
    self.grey_matter_options = GreyMatterWritingOptions(dartel_normalization)
    self.grey_matter_options.setModulationToNonLinear()
    self.white_matter_options = WhiteMatterWritingOptions(dartel_normalization)
    self.white_matter_options.setModulationToNonLinear()
    self.csf_matter_options = CSFMatterWritingOptions(dartel_normalization)
    self.bias_corrected_options = BiasCorrectedWritingOptions(dartel_normalization)
    self.pve_label_options = PVELabelWritingOptions(dartel_normalization)

    self.save_jacobian_warped = 0
    self.deformation_fields = [0, 0]

    if dartel_normalization:
      self.jacobian_prefix = "jac_wrp1"
      self.deformation_field_prefix = "y_r"
      self.inverse_deformation_field_prefix = "iy_r"
    else:
      self.deformation_field_prefix = "y_"
      self.inverse_deformation_field_prefix = "iy_"

    self.deformation_matrix_suffix="_seg8"
    self.deformation_matrix_extension="mat"
    self.matter_volumes_prefix = "p"
    self.matter_volumes_suffix = "_seg8"
    self.matter_volumes_extension = "txt"

    self.jacobian_path = None
    self.deformation_field_path = None
    self.inverse_deformation_field_path = None
    self.deformation_matrix_path = None
    self.matter_volumes_path = None

  def discardJacobianNormalized(self):
    """
    This   is   the  option  to  save  the  Jacobian  determinant,  which  expresses  local  volume
    changes.  This  image  can  be  used  in  a  pure  deformation  based  morphometry (DBM)
    design.
    """
    self.save_jacobian_warped = 0

  def saveJacobianNormalized(self):
    """
    This   is   the  option  to  save  the  Jacobian  determinant,  which  expresses  local  volume
    changes.  This  image  can  be  used  in  a  pure  deformation  based  morphometry (DBM)
    design.
    """
    self.save_jacobian_warped = 1

  def discardDeformationField(self):
    """
    Deformation fields can be saved to disk, and used by the Deformations Utility. For spatially
    normalising  images  to  MNI  space,  you  will  need the forward deformation, whereas for
    spatially  normalising  (eg)  GIFTI  surface files, you'll need the inverse. It is also possible to
    transform  data  in  MNI space on to the individual subject, which also requires the inverse
    transform.  Deformations  are  saved  as  .nii files, which contain three volumes to encode
    the x, y and z coordinates.
    """
    self.deformation_fields = [0, 0]

  def saveDeformationFieldInverse(self):
    self.deformation_fields = [0, 1]

  def saveDeformationFieldForward(self):
    """
    Forward deformations can be used to warp an image from native space to Dartel MNI space
    (if Dartel normalization is used) or to the MNI space of the TPM image (for low-dimensional warping).
    The backward deformations can be used to warp an image from Dartel MNI space or TPM MNI
    space to native space. As you suggested these deformations can be used to warp predefined atlases
    to native space. Another application is to warp coregistered fMRI data to Dartel MNI space.
    Volumes should be calulated rather based on native space images than modulated normalized images
    (although the values should be similiar). Again, probabilities can be summed up to consider values >1.
    """
    self.deformation_fields = [1, 0]

  def saveDeformationFieldInverseAndForward(self):
    self.deformation_fields = [1, 1]

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setJacobianPath(self, jacobian_path):
    if self.dartel_normalization:
      self.jacobian_path = jacobian_path
    else:
      raise Exception("Jacobian is writing only if dartel template is used")

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setDeformationFieldPath(self, deformation_field_path):
    self.deformation_field_path = deformation_field_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setInverseDeformationFieldPath(self, inverse_deformation_field_path):
    self.inverse_deformation_field_path = inverse_deformation_field_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setDeformationMatrixPath(self, deformation_matrix_path):
    self.deformation_matrix_path = deformation_matrix_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setMatterVolumesPath(self, matter_volumes_path):
    self.matter_volumes_path = matter_volumes_path
#===============================================================================
  @checkIfArgumentTypeIsAllowed(GreyMatterWritingOptions, 1)
  def replaceGreyMatterWritingOptions(self, grey_matter_options):
    del self.grey_matter_options
    self.grey_matter_options = grey_matter_options

  @checkIfArgumentTypeIsAllowed(WhiteMatterWritingOptions, 1)
  def replaceWhiteMatterWritingOptions(self, white_matter_options):
    del self.white_matter_options
    self.white_matter_options = white_matter_options

  @checkIfArgumentTypeIsAllowed(CSFMatterWritingOptions, 1)
  def replaceCSFMatterWritingOptions(self, csf_matter_options):
    del self.csf_matter_options
    self.csf_matter_options = csf_matter_options

  @checkIfArgumentTypeIsAllowed(BiasCorrectedWritingOptions, 1)
  def replaceBiasCorrectedWritingOptions(self, bias_corrected_options):
    del self.bias_corrected_options
    self.bias_corrected_options = bias_corrected_options

  @checkIfArgumentTypeIsAllowed(PVELabelWritingOptions, 1)
  def replacePVELabelWritingOptions(self, pve_label_options):
    del self.pve_label_options
    self.pve_label_options = pve_label_options

  def getStringListForBatch(self):
    batch_list = []
    batch_list.extend(addBatchKeyWordInEachItem("output", self.grey_matter_options.getStringListForBatch()))
    batch_list.extend(addBatchKeyWordInEachItem("output", self.white_matter_options.getStringListForBatch()))
    batch_list.extend(addBatchKeyWordInEachItem("output", self.csf_matter_options.getStringListForBatch()))
    batch_list.extend(addBatchKeyWordInEachItem("output", self.bias_corrected_options.getStringListForBatch()))
    batch_list.extend(addBatchKeyWordInEachItem("output", self.pve_label_options.getStringListForBatch()))
    batch_list.append("output.jacobian.warped = %s;" % self.save_jacobian_warped)
    batch_list.append("output.warps = %s;" % convertlistToSPMString(self.deformation_fields))
    return batch_list

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def moveSPMDefaultPathsIfNeeded(self, volume_reference_path):
    self.grey_matter_options.moveSPMDefaultPathsIfNeeded(volume_reference_path)
    self.white_matter_options.moveSPMDefaultPathsIfNeeded(volume_reference_path)
    self.csf_matter_options.moveSPMDefaultPathsIfNeeded(volume_reference_path)
    self.bias_corrected_options.moveSPMDefaultPathsIfNeeded(volume_reference_path)
    self.pve_label_options.moveSPMDefaultPathsIfNeeded(volume_reference_path)

    if self.dartel_normalization:
      if self.jacobian_path is not None:
        moveSPMPath(volume_reference_path,
                    self.jacobian_path,
                    prefix=self.jacobian_prefix)

    if self.deformation_field_path is not None:
      moveSPMPath(volume_reference_path,
                  self.deformation_field_path,
                  prefix=self.deformation_field_prefix)
    if self.inverse_deformation_field_path is not None:
      moveSPMPath(volume_reference_path,
                  self.inverse_deformation_field_path,
                  prefix=self.inverse_deformation_field_prefix)
    if self.deformation_matrix_path is not None:
      moveSPMPath(volume_reference_path,
                  self.deformation_matrix_path,
                  suffix=self.deformation_matrix_suffix,
                  extension=self.deformation_matrix_extension)
    if self.matter_volumes_path is not None:
      moveSPMPath(volume_reference_path,
                  self.matter_volumes_path,
                  prefix=self.matter_volumes_prefix,
                  suffix=self.matter_volumes_suffix,
                  extension=self.matter_volumes_extension)
