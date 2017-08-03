# -*- coding: utf-8 -*-

from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.spm_batch_maker_utils import moveSPMPath, convertlistToSPMString
from soma.spm.spm_batch_maker_utils import convertPathListToSPMBatchString

class Channel():
  """
  Specify  a  channel  for  processing.  If  multiple  channels are used (eg PD & T2), then the
  same  order  of  subjects  must be specified for each channel and they must be in register
  (same  position,  size, voxel dims etc..). The different channels can be treated differently in
  terms  of inhomogeneity correction etc. You may wish to correct some channels and save
  the corrected images, whereas you may wish not to do this for other channels.
  """
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setVolumePathList(self, volume_path_list):
    """
    Select  scans  from  this  channel for processing. If multiple channels are used (eg
    T1 & T2), then the same order of subjects must be specified for each channel and
    they must be in register (same position, size, voxel dims etc..).
    """
    self.volume_path_list = volume_path_list

  def getVolumePathList(self):
    return self.volume_path_list

  def unsetBiasRegularisation(self):
    """
    MR  images  are  usually  corrupted  by  a  smooth,  spatially  varying artifact that
    modulates  the intensity of the image (bias). These artifacts, although not usually
    a problem for visual inspection, can impede automated processing of the images.
    An  important  issue  relates  to  the  distinction between intensity variations that
    arise  because  of  bias artifact due to the physics of MR scanning, and those that
    arise  due  to  different  tissue  properties.  The objective is to model the latter by
    different  tissue  classes,  while modelling the former with a bias field. We know a
    priori  that  intensity  variations  due  to  MR physics tend to be spatially smooth,
    whereas  those  due to different tissue types tend to contain more high frequency
    information. A more accurate estimate of a bias field can be obtained by including
    prior  knowledge  about  the  distribution of the fields likely to be encountered by
    the  correction  algorithm.  For  example,  if  it  is  known that there is little or no
    intensity  non-uniformity,  then  it  would be wise to penalise large values for the
    intensity  non-uniformity  parameters.  This  regularisation can be placed within a
    Bayesian  context,  whereby  the  penalty  incurred  is the negative logarithm of a
    prior probability for any particular pattern of non-uniformity.
    Knowing  what  works  best  should  be  a  matter  of  empirical  exploration.  For
    example,  if  your  data  has  very little intensity non-uniformity artifact, then the
    bias  regularisation  should  be increased.  This effectively tells the algorithm that
    there is very little bias in your data, so it does not try to model it.
    """
    self.bias_regularisation = 0

  def setBiasRegularisationToExtremelyLight(self):
    """
    MR  images  are  usually  corrupted  by  a  smooth,  spatially  varying artifact that
    modulates  the intensity of the image (bias). These artifacts, although not usually
    a problem for visual inspection, can impede automated processing of the images.
    An  important  issue  relates  to  the  distinction between intensity variations that
    arise  because  of  bias artifact due to the physics of MR scanning, and those that
    arise  due  to  different  tissue  properties.  The objective is to model the latter by
    different  tissue  classes,  while modelling the former with a bias field. We know a
    priori  that  intensity  variations  due  to  MR physics tend to be spatially smooth,
    whereas  those  due to different tissue types tend to contain more high frequency
    information. A more accurate estimate of a bias field can be obtained by including
    prior  knowledge  about  the  distribution of the fields likely to be encountered by
    the  correction  algorithm.  For  example,  if  it  is  known that there is little or no
    intensity  non-uniformity,  then  it  would be wise to penalise large values for the
    intensity  non-uniformity  parameters.  This  regularisation can be placed within a
    Bayesian  context,  whereby  the  penalty  incurred  is the negative logarithm of a
    prior probability for any particular pattern of non-uniformity.
    Knowing  what  works  best  should  be  a  matter  of  empirical  exploration.  For
    example,  if  your  data  has  very little intensity non-uniformity artifact, then the
    bias  regularisation  should  be increased.  This effectively tells the algorithm that
    there is very little bias in your data, so it does not try to model it.
    """
    self.bias_regularisation = 0.00001

  def setBiasRegularisationToVeryLight(self):
    """
    MR  images  are  usually  corrupted  by  a  smooth,  spatially  varying artifact that
    modulates  the intensity of the image (bias). These artifacts, although not usually
    a problem for visual inspection, can impede automated processing of the images.
    An  important  issue  relates  to  the  distinction between intensity variations that
    arise  because  of  bias artifact due to the physics of MR scanning, and those that
    arise  due  to  different  tissue  properties.  The objective is to model the latter by
    different  tissue  classes,  while modelling the former with a bias field. We know a
    priori  that  intensity  variations  due  to  MR physics tend to be spatially smooth,
    whereas  those  due to different tissue types tend to contain more high frequency
    information. A more accurate estimate of a bias field can be obtained by including
    prior  knowledge  about  the  distribution of the fields likely to be encountered by
    the  correction  algorithm.  For  example,  if  it  is  known that there is little or no
    intensity  non-uniformity,  then  it  would be wise to penalise large values for the
    intensity  non-uniformity  parameters.  This  regularisation can be placed within a
    Bayesian  context,  whereby  the  penalty  incurred  is the negative logarithm of a
    prior probability for any particular pattern of non-uniformity.
    Knowing  what  works  best  should  be  a  matter  of  empirical  exploration.  For
    example,  if  your  data  has  very little intensity non-uniformity artifact, then the
    bias  regularisation  should  be increased.  This effectively tells the algorithm that
    there is very little bias in your data, so it does not try to model it.
    """
    self.bias_regularisation = 0.0001

  def setBiasRegularisationToLight(self):
    """
    MR  images  are  usually  corrupted  by  a  smooth,  spatially  varying artifact that
    modulates  the intensity of the image (bias). These artifacts, although not usually
    a problem for visual inspection, can impede automated processing of the images.
    An  important  issue  relates  to  the  distinction between intensity variations that
    arise  because  of  bias artifact due to the physics of MR scanning, and those that
    arise  due  to  different  tissue  properties.  The objective is to model the latter by
    different  tissue  classes,  while modelling the former with a bias field. We know a
    priori  that  intensity  variations  due  to  MR physics tend to be spatially smooth,
    whereas  those  due to different tissue types tend to contain more high frequency
    information. A more accurate estimate of a bias field can be obtained by including
    prior  knowledge  about  the  distribution of the fields likely to be encountered by
    the  correction  algorithm.  For  example,  if  it  is  known that there is little or no
    intensity  non-uniformity,  then  it  would be wise to penalise large values for the
    intensity  non-uniformity  parameters.  This  regularisation can be placed within a
    Bayesian  context,  whereby  the  penalty  incurred  is the negative logarithm of a
    prior probability for any particular pattern of non-uniformity.
    Knowing  what  works  best  should  be  a  matter  of  empirical  exploration.  For
    example,  if  your  data  has  very little intensity non-uniformity artifact, then the
    bias  regularisation  should  be increased.  This effectively tells the algorithm that
    there is very little bias in your data, so it does not try to model it.
    """
    self.bias_regularisation = 0.001

  def setBiasRegularisationToMedium(self):
    """
    MR  images  are  usually  corrupted  by  a  smooth,  spatially  varying artifact that
    modulates  the intensity of the image (bias). These artifacts, although not usually
    a problem for visual inspection, can impede automated processing of the images.
    An  important  issue  relates  to  the  distinction between intensity variations that
    arise  because  of  bias artifact due to the physics of MR scanning, and those that
    arise  due  to  different  tissue  properties.  The objective is to model the latter by
    different  tissue  classes,  while modelling the former with a bias field. We know a
    priori  that  intensity  variations  due  to  MR physics tend to be spatially smooth,
    whereas  those  due to different tissue types tend to contain more high frequency
    information. A more accurate estimate of a bias field can be obtained by including
    prior  knowledge  about  the  distribution of the fields likely to be encountered by
    the  correction  algorithm.  For  example,  if  it  is  known that there is little or no
    intensity  non-uniformity,  then  it  would be wise to penalise large values for the
    intensity  non-uniformity  parameters.  This  regularisation can be placed within a
    Bayesian  context,  whereby  the  penalty  incurred  is the negative logarithm of a
    prior probability for any particular pattern of non-uniformity.
    Knowing  what  works  best  should  be  a  matter  of  empirical  exploration.  For
    example,  if  your  data  has  very little intensity non-uniformity artifact, then the
    bias  regularisation  should  be increased.  This effectively tells the algorithm that
    there is very little bias in your data, so it does not try to model it.
    """
    self.bias_regularisation = 0.01

  def setBiasRegularisationToHeavy(self):
    """
    MR  images  are  usually  corrupted  by  a  smooth,  spatially  varying artifact that
    modulates  the intensity of the image (bias). These artifacts, although not usually
    a problem for visual inspection, can impede automated processing of the images.
    An  important  issue  relates  to  the  distinction between intensity variations that
    arise  because  of  bias artifact due to the physics of MR scanning, and those that
    arise  due  to  different  tissue  properties.  The objective is to model the latter by
    different  tissue  classes,  while modelling the former with a bias field. We know a
    priori  that  intensity  variations  due  to  MR physics tend to be spatially smooth,
    whereas  those  due to different tissue types tend to contain more high frequency
    information. A more accurate estimate of a bias field can be obtained by including
    prior  knowledge  about  the  distribution of the fields likely to be encountered by
    the  correction  algorithm.  For  example,  if  it  is  known that there is little or no
    intensity  non-uniformity,  then  it  would be wise to penalise large values for the
    intensity  non-uniformity  parameters.  This  regularisation can be placed within a
    Bayesian  context,  whereby  the  penalty  incurred  is the negative logarithm of a
    prior probability for any particular pattern of non-uniformity.
    Knowing  what  works  best  should  be  a  matter  of  empirical  exploration.  For
    example,  if  your  data  has  very little intensity non-uniformity artifact, then the
    bias  regularisation  should  be increased.  This effectively tells the algorithm that
    there is very little bias in your data, so it does not try to model it.
    """
    self.bias_regularisation = 0.1

  def setBiasRegularisationToVeryHeavy(self):
    """
    MR  images  are  usually  corrupted  by  a  smooth,  spatially  varying artifact that
    modulates  the intensity of the image (bias). These artifacts, although not usually
    a problem for visual inspection, can impede automated processing of the images.
    An  important  issue  relates  to  the  distinction between intensity variations that
    arise  because  of  bias artifact due to the physics of MR scanning, and those that
    arise  due  to  different  tissue  properties.  The objective is to model the latter by
    different  tissue  classes,  while modelling the former with a bias field. We know a
    priori  that  intensity  variations  due  to  MR physics tend to be spatially smooth,
    whereas  those  due to different tissue types tend to contain more high frequency
    information. A more accurate estimate of a bias field can be obtained by including
    prior  knowledge  about  the  distribution of the fields likely to be encountered by
    the  correction  algorithm.  For  example,  if  it  is  known that there is little or no
    intensity  non-uniformity,  then  it  would be wise to penalise large values for the
    intensity  non-uniformity  parameters.  This  regularisation can be placed within a
    Bayesian  context,  whereby  the  penalty  incurred  is the negative logarithm of a
    prior probability for any particular pattern of non-uniformity.
    Knowing  what  works  best  should  be  a  matter  of  empirical  exploration.  For
    example,  if  your  data  has  very little intensity non-uniformity artifact, then the
    bias  regularisation  should  be increased.  This effectively tells the algorithm that
    there is very little bias in your data, so it does not try to model it.
    """
    self.bias_regularisation = 1

  def setBiasRegularisationToExtremelyHeavy(self):
    """
    MR  images  are  usually  corrupted  by  a  smooth,  spatially  varying artifact that
    modulates  the intensity of the image (bias). These artifacts, although not usually
    a problem for visual inspection, can impede automated processing of the images.
    An  important  issue  relates  to  the  distinction between intensity variations that
    arise  because  of  bias artifact due to the physics of MR scanning, and those that
    arise  due  to  different  tissue  properties.  The objective is to model the latter by
    different  tissue  classes,  while modelling the former with a bias field. We know a
    priori  that  intensity  variations  due  to  MR physics tend to be spatially smooth,
    whereas  those  due to different tissue types tend to contain more high frequency
    information. A more accurate estimate of a bias field can be obtained by including
    prior  knowledge  about  the  distribution of the fields likely to be encountered by
    the  correction  algorithm.  For  example,  if  it  is  known that there is little or no
    intensity  non-uniformity,  then  it  would be wise to penalise large values for the
    intensity  non-uniformity  parameters.  This  regularisation can be placed within a
    Bayesian  context,  whereby  the  penalty  incurred  is the negative logarithm of a
    prior probability for any particular pattern of non-uniformity.
    Knowing  what  works  best  should  be  a  matter  of  empirical  exploration.  For
    example,  if  your  data  has  very little intensity non-uniformity artifact, then the
    bias  regularisation  should  be increased.  This effectively tells the algorithm that
    there is very little bias in your data, so it does not try to model it.
    """
    self.bias_regularisation = 10

  def unsetBiasFWHM(self):
    """
    FWHM  of  Gaussian  smoothness of bias. If your intensity non-uniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity  non-uniformity  is  one of i.i.d. Gaussian noise that has been smoothed
    by  some  amount,  before  taking  the exponential. Note also that smoother bias
    fields  need  fewer parameters to describe them. This means that the algorithm is
    faster for smoother intensity non-uniformities.
    """
    self.bias_FWHM = 'Inf'

  def setBiasFWHMTo30cutoff(self):
    """
    FWHM  of  Gaussian  smoothness of bias. If your intensity non-uniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity  non-uniformity  is  one of i.i.d. Gaussian noise that has been smoothed
    by  some  amount,  before  taking  the exponential. Note also that smoother bias
    fields  need  fewer parameters to describe them. This means that the algorithm is
    faster for smoother intensity non-uniformities.
    """
    self.bias_FWHM = '30'

  def setBiasFWHMTo40cutoff(self):
    """
    FWHM  of  Gaussian  smoothness of bias. If your intensity non-uniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity  non-uniformity  is  one of i.i.d. Gaussian noise that has been smoothed
    by  some  amount,  before  taking  the exponential. Note also that smoother bias
    fields  need  fewer parameters to describe them. This means that the algorithm is
    faster for smoother intensity non-uniformities.
    """
    self.bias_FWHM = '40'

  def setBiasFWHMTo50cutoff(self):
    """
    FWHM  of  Gaussian  smoothness of bias. If your intensity non-uniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity  non-uniformity  is  one of i.i.d. Gaussian noise that has been smoothed
    by  some  amount,  before  taking  the exponential. Note also that smoother bias
    fields  need  fewer parameters to describe them. This means that the algorithm is
    faster for smoother intensity non-uniformities.
    """
    self.bias_FWHM = '50'

  def setBiasFWHMTo60cutoff(self):
    """
    FWHM  of  Gaussian  smoothness of bias. If your intensity non-uniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity  non-uniformity  is  one of i.i.d. Gaussian noise that has been smoothed
    by  some  amount,  before  taking  the exponential. Note also that smoother bias
    fields  need  fewer parameters to describe them. This means that the algorithm is
    faster for smoother intensity non-uniformities.
    """
    self.bias_FWHM = '60'

  def setBiasFWHMTo70cutoff(self):
    """
    FWHM  of  Gaussian  smoothness of bias. If your intensity non-uniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity  non-uniformity  is  one of i.i.d. Gaussian noise that has been smoothed
    by  some  amount,  before  taking  the exponential. Note also that smoother bias
    fields  need  fewer parameters to describe them. This means that the algorithm is
    faster for smoother intensity non-uniformities.
    """
    self.bias_FWHM = '70'

  def setBiasFWHMTo80cutoff(self):
    """
    FWHM  of  Gaussian  smoothness of bias. If your intensity non-uniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity  non-uniformity  is  one of i.i.d. Gaussian noise that has been smoothed
    by  some  amount,  before  taking  the exponential. Note also that smoother bias
    fields  need  fewer parameters to describe them. This means that the algorithm is
    faster for smoother intensity non-uniformities.
    """
    self.bias_FWHM = '80'

  def setBiasFWHMTo90cutoff(self):
    """
    FWHM  of  Gaussian  smoothness of bias. If your intensity non-uniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity  non-uniformity  is  one of i.i.d. Gaussian noise that has been smoothed
    by  some  amount,  before  taking  the exponential. Note also that smoother bias
    fields  need  fewer parameters to describe them. This means that the algorithm is
    faster for smoother intensity non-uniformities.
    """
    self.bias_FWHM = '90'

  def setBiasFWHMTo100cutoff(self):
    """
    FWHM  of  Gaussian  smoothness of bias. If your intensity non-uniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity  non-uniformity  is  one of i.i.d. Gaussian noise that has been smoothed
    by  some  amount,  before  taking  the exponential. Note also that smoother bias
    fields  need  fewer parameters to describe them. This means that the algorithm is
    faster for smoother intensity non-uniformities.
    """
    self.bias_FWHM = '100'

  def setBiasFWHMTo110cutoff(self):
    """
    FWHM  of  Gaussian  smoothness of bias. If your intensity non-uniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity  non-uniformity  is  one of i.i.d. Gaussian noise that has been smoothed
    by  some  amount,  before  taking  the exponential. Note also that smoother bias
    fields  need  fewer parameters to describe them. This means that the algorithm is
    faster for smoother intensity non-uniformities.
    """
    self.bias_FWHM = '110'

  def setBiasFWHMTo120cutoff(self):
    """
    FWHM  of  Gaussian  smoothness of bias. If your intensity non-uniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity  non-uniformity  is  one of i.i.d. Gaussian noise that has been smoothed
    by  some  amount,  before  taking  the exponential. Note also that smoother bias
    fields  need  fewer parameters to describe them. This means that the algorithm is
    faster for smoother intensity non-uniformities.
    """
    self.bias_FWHM = '120'

  def setBiasFWHMTo130cutoff(self):
    """
    FWHM  of  Gaussian  smoothness of bias. If your intensity non-uniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity  non-uniformity  is  one of i.i.d. Gaussian noise that has been smoothed
    by  some  amount,  before  taking  the exponential. Note also that smoother bias
    fields  need  fewer parameters to describe them. This means that the algorithm is
    faster for smoother intensity non-uniformities.
    """
    self.bias_FWHM = '130'

  def setBiasFWHMTo140cutoff(self):
    """
    FWHM  of  Gaussian  smoothness of bias. If your intensity non-uniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity  non-uniformity  is  one of i.i.d. Gaussian noise that has been smoothed
    by  some  amount,  before  taking  the exponential. Note also that smoother bias
    fields  need  fewer parameters to describe them. This means that the algorithm is
    faster for smoother intensity non-uniformities.
    """
    self.bias_FWHM = '140'

  def setBiasFWHMTo150cutoff(self):
    """
    FWHM  of  Gaussian  smoothness of bias. If your intensity non-uniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity  non-uniformity  is  one of i.i.d. Gaussian noise that has been smoothed
    by  some  amount,  before  taking  the exponential. Note also that smoother bias
    fields  need  fewer parameters to describe them. This means that the algorithm is
    faster for smoother intensity non-uniformities.
    """
    self.bias_FWHM = '150'

  def saveBiasCorrected(self):
    """
    This  is  the  option  to  save  a  bias  corrected  version of your images from this
    channel,  or/and  the  estimated  bias  field. MR images are usually corrupted by a
    smooth, spatially varying artifact that modulates the intensity of the image (bias).
    These  artifacts, although not usually a problem for visual inspection, can impede
    automated  processing  of  the  images.    The bias corrected version should have
    more uniform intensities within the different types of tissues.
    """
    self.save_bias_corrected = [0, 1]

  def discardBiasCorrected(self):
    """
    This  is  the  option  to  save  a  bias  corrected  version of your images from this
    channel,  or/and  the  estimated  bias  field. MR images are usually corrupted by a
    smooth, spatially varying artifact that modulates the intensity of the image (bias).
    These  artifacts, although not usually a problem for visual inspection, can impede
    automated  processing  of  the  images.    The bias corrected version should have
    more uniform intensities within the different types of tissues.
    """
    self.save_bias_corrected = [0, 0]

  def saveBiasField(self):
    """
    This  is  the  option  to  save  a  bias  corrected  version of your images from this
    channel,  or/and  the  estimated  bias  field. MR images are usually corrupted by a
    smooth, spatially varying artifact that modulates the intensity of the image (bias).
    These  artifacts, although not usually a problem for visual inspection, can impede
    automated  processing  of  the  images.    The bias corrected version should have
    more uniform intensities within the different types of tissues.
    """
    self.save_bias_corrected = [1, 0]

  def saveBiasFieldAndBiasCorrected(self):
    """
    This  is  the  option  to  save  a  bias  corrected  version of your images from this
    channel,  or/and  the  estimated  bias  field. MR images are usually corrupted by a
    smooth, spatially varying artifact that modulates the intensity of the image (bias).
    These  artifacts, although not usually a problem for visual inspection, can impede
    automated  processing  of  the  images.    The bias corrected version should have
    more uniform intensities within the different types of tissues.
    """
    self.save_bias_corrected = [1, 1]

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setBiasCorrectedPathList(self, output_path_list):
    self.bias_corrected_path_list = output_path_list

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setBiasFieldPath(self, output_path_list):
    self.bias_field_path_list = output_path_list

  def getStringListForBatch(self):
    if self.volume_path_list:
      batch_list = []
      batch_list.append("vols = {%s};" % convertPathListToSPMBatchString(self.volume_path_list))
      batch_list.append("biasreg = %g;" % self.bias_regularisation)
      batch_list.append("biasfwhm = %s;" % self.bias_FWHM)
      batch_list.append("write = %s;" % convertlistToSPMString(self.save_bias_corrected))
      return batch_list
    else:
      raise ValueError('Channel volume is required')

  def moveBiasSavingIfNeeded(self):
    if self.bias_corrected_path_list:
      for volume_path, bias_corrected_path in zip(self.volume_path_list,
                                                  self.bias_corrected_path_list):
        moveSPMPath(volume_path,
                    bias_corrected_path,
                    prefix=self.bias_corrected_prefix)
    if self.bias_field_path_list:
      for volume_path, bias_field_path in zip(self.volume_path_path,
                                              self.bias_field_path_list):
        moveSPMPath(volume_path,
                    bias_field_path,
                    prefix=self.bias_field_prefix)