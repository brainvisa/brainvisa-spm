# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm_main_module import SPM12MainModule
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
from soma.spm.spm_batch_maker_utils import convertPathListToSPMBatchString, convertlistToSPMString
from soma.spm.spm_batch_maker_utils import convertNumpyArrayToSPMString, moveSPMPath
import numpy
import numbers
from six.moves import zip

class SerialLongitudinalRegistration(SPM12MainModule):
  """
  Longitudinal registration of series of anatomical MRI scans for a single subject.  It
  is   based  on  groupwise  alignment  among  each  of  the  subject's  scans,  and
  incorporates  a  bias  field correction.  Prior to running the registration, the scans
  should   already   be   in   very   rough  alignment,  although  because  the  model
  incorporates  a  rigid-body  transform,  this need not be extremely precise.  Note
  that  there  are  a  bunch  of hyper-parameters to be specified.  If you are unsure
  what  values  to  take,  then  the  defaults  should  be a reasonable guess of what
  works.    Note  that  changes  to  these  hyper-parameters will impact the results
  obtained.
  The  alignment  assumes  that  all scans have similar resolutions and dimensions,
  and were collected on the same (or very similar) MR scanner using the same pulse
  sequence.    If  these assumption are not correct, then the approach will not work
  as well.
  """
  def __init__(self):
    self.volume_path_list = None
    self.time_list = None
    self.noise_estimate = "NaN"
    self.warping_regularisation_list = [0, 0, 100, 25, 100]
    self.bias_regularisation = 1000000
    self.save_mid_point_average = 1
    self.save_jacobian_rate = 0
    self.save_divergence_rate = 1
    self.save_deformation_fields = 0

    self.ouput_mid_point_average_path = None
    self.ouput_jacobian_rate_path_list = None
    self.ouput_divergence_rate_path_list = None
    self.ouput_volume_deformation_field_path_list = None

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def appendVolume(self, volume_path):
    """
    Select scans for this subject.
    """
    if self.volume_path_list is not None:
      self.volume_path_list.append(volume_path)
    else:
      self.volume_path_list = [volume_path]

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setVolumes(self, volume_path_list):
    """
    Specify the times of the scans in years.
    """
    for volume_path in volume_path_list:
      self.appendVolume(volume_path)

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setTimes(self, time_list):
    """
    Specify  the time difference between the scans in years.  This can be a single value (if it
    is the same for all subjects) or a vector of values (if it differs among subjects).
    """
    self.time_list = time_list

  @checkIfArgumentTypeIsAllowed(numpy.ndarray, 1)
  def setNoiseEstimate(self, noise_estimate_numpy_array):
    """
    Specify  the  standard  deviation  of  the  noise  in the images.  If a scalar is entered, all
    images  will be assumed to have the same level of noise.  For any non-finite values, the
    algorithm  will  try to estimate reasonable noise estimates based on fitting a mixture of
    two  Rician  distributions  to  the intensity histogram of each of the images. This works
    reasonably  well  for  simple  MRI  scans,  but  less  well  for  derived  images  (such  as
    averages).    The  assumption  is  that the residuals, after fitting the registration model,
    are i.i.d. Gaussian.
    """
    self.noise_estimate = convertNumpyArrayToSPMString(noise_estimate_numpy_array)

  def setNoiseEstimateToNaN(self):
    """
    Specify  the  standard  deviation  of  the  noise  in the images.  If a scalar is entered, all
    images  will be assumed to have the same level of noise.  For any non-finite values, the
    algorithm  will  try to estimate reasonable noise estimates based on fitting a mixture of
    two  Rician  distributions  to  the intensity histogram of each of the images. This works
    reasonably  well  for  simple  MRI  scans,  but  less  well  for  derived  images  (such  as
    averages).    The  assumption  is  that the residuals, after fitting the registration model,
    are i.i.d. Gaussian.
    """
    self.noise_estimate = "NaN"

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setWarpingRegulariation(self, warping_regularisation_list):
    """
    Registration  involves simultaneously minimising two terms.  One of these is a measure
    of  similarity  between  the  images  (mean-squared difference in the current situation),
    whereas the other is a measure of the roughness of the deformations.  This measure of
    roughness involves the sum of the following terms:
    * Absolute  displacements  need  to  be  penalised  by  a tiny amount.  The first element
      encodes  the  amount of penalty on these.  Ideally, absolute displacements should not
      be penalised, but it is necessary for technical reasons.
    * The  `membrane  energy'  of  the deformation is penalised (2nd element), usually by a
      relatively  small  amount.  This  penalises the sum of squares of the derivatives of the
      velocity field (ie the sum of squares of the elements of the Jacobian tensors).
    * The  `bending energy' is penalised (3rd element). This penalises the sum of squares of
      the 2nd derivatives of the velocity.
    * Linear  elasticity  regularisation  is  also  included  (4th  and  5th  elements).  The first
      parameter  (mu)  is  similar  to that for linear elasticity, except it penalises the sum of
      squares  of  the  Jacobian tensors after they have been made symmetric (by averaging
      with   the   transpose).      This  term  essentially  penalises  length  changes,  without
      penalising rotations.
    * The  final  term  also  relates  to  linear  elasticity, and is the weight that denotes how
      much   to   penalise   changes  to  the  divergence  of  the  velocities  (lambda).    This
      divergence is a measure of the rate of volumetric expansion or contraction.
    Note  that  regularisation  is  specified based on what is believed to be appropriate for a
    year   of  growth.    The  specified  values  are  divided  by  the  number  of  years  time
    difference.
    """
    if len(warping_regularisation_list) == 5:
      self.warping_regularisation_list = warping_regularisation_list
    else:
      raise ValueError("Unvalid warping_regularisation_list : 5 fields is required")

  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
  def setBiasRegularisation(self, bias_regularisation):
    """
    MR  images are usually corrupted by a smooth, spatially varying artifact that modulates
    the  intensity  of  the  image  (bias). These artifacts, although not usually a problem for
    visual inspection, can impede automated processing of the images.
    An  important  issue  relates  to  the  distinction  between  variations  in  the difference
    between  the  images  that  arise  because  of  the  differential  bias  artifact due to the
    physics of MR scanning, and those that arise due to shape differences.  The objective is
    to  model  the  latter  by deformations, while modelling the former with a bias field. We
    know a priori that intensity variations due to MR physics tend to be spatially smooth. A
    more  accurate  estimate  of  a  bias  field can be obtained by including prior knowledge
    about the distribution of the fields likely to be encountered by the correction algorithm.
    For  example,  if  it  is  known that there is little or no intensity non-uniformity, then it
    would be wise to penalise large estimates of the intensity non-uniformity.
    Knowing what works best should be a matter of empirical exploration, as it depends on
    the  scans themselves.  For example, if your data has very little of the artifact, then the
    bias regularisation should be increased.  This effectively tells the algorithm that there is
    very little bias in your data, so it does not try to model it.
    """
    self.bias_regularisation = bias_regularisation

  def saveMidPointAverage(self):
    """
    Do  you  want to save the mid-point average template image? This is likely to be useful
    for  groupwise  alignment,  and  is  prefixed  by  ``avg_''  and  written  out in the same
    directory of the first time point data.
    """
    self.save_mid_point_average = True

  def discardMidPointAverage(self):
    """
    Do  you  want to save the mid-point average template image? This is likely to be useful
    for  groupwise  alignment,  and  is  prefixed  by  ``avg_''  and  written  out in the same
    directory of the first time point data.
    """
    self.save_mid_point_average = False

  def saveJacobianRate(self):
    """
    Do  you  want  to  save  a  map  of  the differences between the Jacobian determinants,
    divided  by  the time interval?  Some consider these useful for morphometrics (although
    Jacobian determinants is computed and this is divided by the time interval. One original
    Jacobian  map is for the deformation from the mid point to the first scan, and the other
    is  for  the  deformation from the mid point to the second scan.  Each of these encodes
    the  relative  volume  (at  each  spatial  location)  between  the  scan and the mid-point
    average.  Values  less  than  0  indicate  contraction (over time), whereas values greater
    than  zero indicate expansion.  These files are prefixed by ``jd_'' and written out in the
    same directory of the first time point data.
    """
    self.save_jacobian_rate = 1

  def discardJacobianRate(self):
    """
    Do  you  want  to  save  a  map  of  the differences between the Jacobian determinants,
    divided  by  the time interval?  Some consider these useful for morphometrics (although
    Jacobian determinants is computed and this is divided by the time interval. One original
    Jacobian  map is for the deformation from the mid point to the first scan, and the other
    is  for  the  deformation from the mid point to the second scan.  Each of these encodes
    the  relative  volume  (at  each  spatial  location)  between  the  scan and the mid-point
    average.  Values  less  than  0  indicate  contraction (over time), whereas values greater
    than  zero indicate expansion.  These files are prefixed by ``jd_'' and written out in the
    same directory of the first time point data.
    """
    self.save_jacobian_rate = 0

  def saveDivergenceRate(self):
    """
    Do  you  want  to  save  a  map  of  divergence  of  the velocity field?  This is useful for
    morphometrics,  and  may be considered as the rate of volumetric expansion.  Negative
    values  indicate  contraction.  These  files  are prefixed by ``dv_'' and written out in the
    same  directory  of the first time point data. Note that the divergences written out have
    been divided by the time interval between scans
    """
    self.save_divergence_rate = 1

  def discardDivergenceRate(self):
    """
    Do  you  want  to  save  a  map  of  divergence  of  the velocity field?  This is useful for
    morphometrics,  and  may be considered as the rate of volumetric expansion.  Negative
    values  indicate  contraction.  These  files  are prefixed by ``dv_'' and written out in the
    same  directory  of the first time point data. Note that the divergences written out have
    been divided by the time interval between scans
    """
    self.save_divergence_rate = 0

  def saveDeformationFields(self):
    """
    Deformation   fields  can  be  saved  to  disk,  and  used  by  the  Deformations  Utility.
    Deformations  are saved as y_*.nii files, which contain three volumes to encode the x, y
    and z coordinates.  They are written in the same directory as the corresponding image.
    """
    self.save_deformation_fields = 1

  def discardDeformationFields(self):
    """
    Deformation   fields  can  be  saved  to  disk,  and  used  by  the  Deformations  Utility.
    Deformations  are saved as y_*.nii files, which contain three volumes to encode the x, y
    and z coordinates.  They are written in the same directory as the corresponding image.
    """
    self.save_deformation_fields = 0

  def getStringListForBatch(self):
    if not None in [self.volume_path_list, self.time_list]:
      if len(self.volume_path_list) == len(self.time_list):
        batch_list = []
        batch_list.append("spm.tools.longit{1}.series.vols = {%s};" % convertPathListToSPMBatchString(self.volume_path_list))
        batch_list.append("spm.tools.longit{1}.series.times = %s;" % convertlistToSPMString( self.time_list))
        batch_list.append("spm.tools.longit{1}.series.noise = %s;" % self.noise_estimate)
        batch_list.append("spm.tools.longit{1}.series.wparam = %s;" % convertlistToSPMString(self.warping_regularisation_list))
        batch_list.append("spm.tools.longit{1}.series.bparam = %g;" % self.bias_regularisation)
        batch_list.append("spm.tools.longit{1}.series.write_avg = %i;" % self.save_mid_point_average)
        batch_list.append("spm.tools.longit{1}.series.write_jac = %i;" % self.save_jacobian_rate)
        batch_list.append("spm.tools.longit{1}.series.write_div = %i;" % self.save_divergence_rate)
        batch_list.append("spm.tools.longit{1}.series.write_def = %i;" % self.save_deformation_fields)
        return batch_list
      else:
        raise ValueError("volume_path_list and time_list has not the same length")
    else:
      raise ValueError("volume_path_list and time_list are required")

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setOutputMidPointAverage(self, output_path):
    self.ouput_mid_point_average_path = output_path

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setOutputJacobianRate(self, output_path_list):
    self.ouput_jacobian_rate_path_list = output_path_list

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setOutputDivergeRate(self, output_path_list):
    self.ouput_divergence_rate_path_list = output_path_list

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setOutputVolumeDeformationField(self, output_path_list):
    self.ouput_volume_deformation_field_path_list = output_path_list

  def _moveSPMDefaultPathsIfNeeded(self):
    if self.ouput_mid_point_average_path is not None and self.save_mid_point_average:
      moveSPMPath(self.volume_path_list[0],
                  self.ouput_mid_point_average_path,
                  prefix='avg_')
    else:
      pass

    if self.ouput_volume_deformation_field_path_list is not None and self.save_deformation_fields:
      if len(self.ouput_volume_deformation_field_path_list) == len(self.volume_path_list):
        for reference_path, output_path in zip(self.volume_path_list, self.ouput_volume_deformation_field_path_list):
          moveSPMPath(reference_path,
                      output_path,
                      prefix='y_')
      else:
        raise ValueError("Unvalid ouput_volume_deformation_field_path_list")
    else:
      pass

    if self.ouput_jacobian_rate_path_list is not None and self.save_jacobian_rate:
      if len(self.ouput_jacobian_rate_path_list) == len(self.volume_path_list):
        for reference_path, output_path in zip(self.volume_path_list, self.ouput_jacobian_rate_path_list):
          moveSPMPath(reference_path,
                      output_path,
                      prefix='j_')
      else:
        raise ValueError("Unvalid ouput_jacobian_rate_path_list")
    else:
      pass

    if self.ouput_divergence_rate_path_list is not None and self.save_divergence_rate:
      if len(self.ouput_divergence_rate_path_list) == len(self.volume_path_list):
        for reference_path, output_path in zip(self.volume_path_list, self.ouput_divergence_rate_path_list):
          moveSPMPath(reference_path,
                      output_path,
                      prefix='dv_')
      else:
        raise ValueError("Unvalid ouput_divergence_rate_path_list")
    else:
      pass

