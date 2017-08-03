 # -*- coding: utf-8 -*-
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed

class BiasCorrectionOptions():
  """
  MR  images  are  usually  corrupted  by  a  smooth,  spatially  varying artifact that
  modulates  the intensity of the image (bias). These artifacts, although not usually
  a problem for visual inspection, can impede automated processing of the images.
  Before registering the images, an approximate bias correction is estimated for the
  moved  image.  This is based on minimising the difference between the images an
  a  symmetric  way.  Prior  to registering the images, they should be rigidly aligned
  together.  The bias correction is estimated once for these aligned images.
  """
  @checkIfArgumentTypeIsAllowed(int, argument_index=1)
  def setIterations(self, iteration):
    """
    Number of iterations for the bias correction
    """
    self.iteration = iteration
    
  def setBiasFWHMTo30mmCutoff(self):
    """
    FWHM  of  Gaussian  smoothness  of  bias. If your intensity nonuniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity nonuniformity is one of i.i.d. Gaussian noise that has been smoothed by
    some  amount, before taking the exponential. Note also that smoother bias fields
    need  fewer parameters to describe them. This means that the algorithm is faster
    for smoother intensity nonuniformities.
    """
    self.bias_fwhm = 30
    
  def setBiasFWHMTo40mmCutoff(self):
    """
    FWHM  of  Gaussian  smoothness  of  bias. If your intensity nonuniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity nonuniformity is one of i.i.d. Gaussian noise that has been smoothed by
    some  amount, before taking the exponential. Note also that smoother bias fields
    need  fewer parameters to describe them. This means that the algorithm is faster
    for smoother intensity nonuniformities.
    """
    self.bias_fwhm = 40
    
  def setBiasFWHMTo50mmCutoff(self):
    """
    FWHM  of  Gaussian  smoothness  of  bias. If your intensity nonuniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity nonuniformity is one of i.i.d. Gaussian noise that has been smoothed by
    some  amount, before taking the exponential. Note also that smoother bias fields
    need  fewer parameters to describe them. This means that the algorithm is faster
    for smoother intensity nonuniformities.
    """
    self.bias_fwhm = 50
    
  def setBiasFWHMTo60mmCutoff(self):
    """
    FWHM  of  Gaussian  smoothness  of  bias. If your intensity nonuniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity nonuniformity is one of i.i.d. Gaussian noise that has been smoothed by
    some  amount, before taking the exponential. Note also that smoother bias fields
    need  fewer parameters to describe them. This means that the algorithm is faster
    for smoother intensity nonuniformities.
    """
    self.bias_fwhm = 60
    
  def setBiasFWHMTo70mmCutoff(self):
    """
    FWHM  of  Gaussian  smoothness  of  bias. If your intensity nonuniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity nonuniformity is one of i.i.d. Gaussian noise that has been smoothed by
    some  amount, before taking the exponential. Note also that smoother bias fields
    need  fewer parameters to describe them. This means that the algorithm is faster
    for smoother intensity nonuniformities.
    """
    self.bias_fwhm = 70
    
  def setBiasFWHMTo80mmCutoff(self):
    """
    FWHM  of  Gaussian  smoothness  of  bias. If your intensity nonuniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity nonuniformity is one of i.i.d. Gaussian noise that has been smoothed by
    some  amount, before taking the exponential. Note also that smoother bias fields
    need  fewer parameters to describe them. This means that the algorithm is faster
    for smoother intensity nonuniformities.
    """
    self.bias_fwhm = 80
    
  def setBiasFWHMTo90mmCutoff(self):
    """
    FWHM  of  Gaussian  smoothness  of  bias. If your intensity nonuniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity nonuniformity is one of i.i.d. Gaussian noise that has been smoothed by
    some  amount, before taking the exponential. Note also that smoother bias fields
    need  fewer parameters to describe them. This means that the algorithm is faster
    for smoother intensity nonuniformities.
    """
    self.bias_fwhm = 90
    
  def setBiasFWHMTo100mmCutoff(self):
    """
    FWHM  of  Gaussian  smoothness  of  bias. If your intensity nonuniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity nonuniformity is one of i.i.d. Gaussian noise that has been smoothed by
    some  amount, before taking the exponential. Note also that smoother bias fields
    need  fewer parameters to describe them. This means that the algorithm is faster
    for smoother intensity nonuniformities.
    """
    self.bias_fwhm = 100
    
  def setBiasFWHMTo110mmCutoff(self):
    """
    FWHM  of  Gaussian  smoothness  of  bias. If your intensity nonuniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity nonuniformity is one of i.i.d. Gaussian noise that has been smoothed by
    some  amount, before taking the exponential. Note also that smoother bias fields
    need  fewer parameters to describe them. This means that the algorithm is faster
    for smoother intensity nonuniformities.
    """
    self.bias_fwhm = 110
    
  def setBiasFWHMTo120mmCutoff(self):
    """
    FWHM  of  Gaussian  smoothness  of  bias. If your intensity nonuniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity nonuniformity is one of i.i.d. Gaussian noise that has been smoothed by
    some  amount, before taking the exponential. Note also that smoother bias fields
    need  fewer parameters to describe them. This means that the algorithm is faster
    for smoother intensity nonuniformities.
    """
    self.bias_fwhm = 120
    
  def setBiasFWHMTo130mmCutoff(self):
    """
    FWHM  of  Gaussian  smoothness  of  bias. If your intensity nonuniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity nonuniformity is one of i.i.d. Gaussian noise that has been smoothed by
    some  amount, before taking the exponential. Note also that smoother bias fields
    need  fewer parameters to describe them. This means that the algorithm is faster
    for smoother intensity nonuniformities.
    """
    self.bias_fwhm = 130
    
  def setBiasFWHMTo140mmCutoff(self):
    """
    FWHM  of  Gaussian  smoothness  of  bias. If your intensity nonuniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity nonuniformity is one of i.i.d. Gaussian noise that has been smoothed by
    some  amount, before taking the exponential. Note also that smoother bias fields
    need  fewer parameters to describe them. This means that the algorithm is faster
    for smoother intensity nonuniformities.
    """
    self.bias_fwhm = 140
    
  def setBiasFWHMTo150mmCutoff(self):
    """
    FWHM  of  Gaussian  smoothness  of  bias. If your intensity nonuniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity nonuniformity is one of i.i.d. Gaussian noise that has been smoothed by
    some  amount, before taking the exponential. Note also that smoother bias fields
    need  fewer parameters to describe them. This means that the algorithm is faster
    for smoother intensity nonuniformities.
    """
    self.bias_fwhm = 150
    
  def unsetBiasFWHM(self):
    """
    FWHM  of  Gaussian  smoothness  of  bias. If your intensity nonuniformity is very
    smooth, then choose a large FWHM. This will prevent the algorithm from trying to
    model   out  intensity  variation  due  to  different  tissue  types.  The  model  for
    intensity nonuniformity is one of i.i.d. Gaussian noise that has been smoothed by
    some  amount, before taking the exponential. Note also that smoother bias fields
    need  fewer parameters to describe them. This means that the algorithm is faster
    for smoother intensity nonuniformities.
    """
    self.bias_fwhm = "Inf"
    
  def setBiasRegularisationToExtremelyLight(self):
    """
    We  know  a  priori that intensity variations due to MR physics tend to be spatially
    smooth,  whereas  those  due  to different tissue types tend to contain more high
    frequency  information.  A  more accurate estimate of a bias field can be obtained
    by  including  prior  knowledge  about  the  distribution  of  the  fields likely to be
    encountered  by the correction algorithm. For example, if it is known that there is
    little  or  no  intensity  non-uniformity,  then  it  would  be  wise to penalise large
    values  for  the  intensity  nonuniformity  parameters.  This  regularisation can be
    placed  within  a  Bayesian  context,  whereby the penalty incurred is the negative
    logarithm of a prior probability for any particular pattern of nonuniformity.
    """
    self.bias_regularisation = 1e-09
    
  def setBiasRegularisationToVeryLight(self):
    """
    We  know  a  priori that intensity variations due to MR physics tend to be spatially
    smooth,  whereas  those  due  to different tissue types tend to contain more high
    frequency  information.  A  more accurate estimate of a bias field can be obtained
    by  including  prior  knowledge  about  the  distribution  of  the  fields likely to be
    encountered  by the correction algorithm. For example, if it is known that there is
    little  or  no  intensity  non-uniformity,  then  it  would  be  wise to penalise large
    values  for  the  intensity  nonuniformity  parameters.  This  regularisation can be
    placed  within  a  Bayesian  context,  whereby the penalty incurred is the negative
    logarithm of a prior probability for any particular pattern of nonuniformity.
    """
    self.bias_regularisation = 1e-08
    
  def setBiasRegularisationToLight(self):
    """
    We  know  a  priori that intensity variations due to MR physics tend to be spatially
    smooth,  whereas  those  due  to different tissue types tend to contain more high
    frequency  information.  A  more accurate estimate of a bias field can be obtained
    by  including  prior  knowledge  about  the  distribution  of  the  fields likely to be
    encountered  by the correction algorithm. For example, if it is known that there is
    little  or  no  intensity  non-uniformity,  then  it  would  be  wise to penalise large
    values  for  the  intensity  nonuniformity  parameters.  This  regularisation can be
    placed  within  a  Bayesian  context,  whereby the penalty incurred is the negative
    logarithm of a prior probability for any particular pattern of nonuniformity.
    """
    self.bias_regularisation = 1e-07
    
  def setBiasRegularisationToMedium(self):
    """
    We  know  a  priori that intensity variations due to MR physics tend to be spatially
    smooth,  whereas  those  due  to different tissue types tend to contain more high
    frequency  information.  A  more accurate estimate of a bias field can be obtained
    by  including  prior  knowledge  about  the  distribution  of  the  fields likely to be
    encountered  by the correction algorithm. For example, if it is known that there is
    little  or  no  intensity  non-uniformity,  then  it  would  be  wise to penalise large
    values  for  the  intensity  nonuniformity  parameters.  This  regularisation can be
    placed  within  a  Bayesian  context,  whereby the penalty incurred is the negative
    logarithm of a prior probability for any particular pattern of nonuniformity.
    """
    self.bias_regularisation = 1e-06
    
  def setBiasRegularisationToHeavy(self):
    """
    We  know  a  priori that intensity variations due to MR physics tend to be spatially
    smooth,  whereas  those  due  to different tissue types tend to contain more high
    frequency  information.  A  more accurate estimate of a bias field can be obtained
    by  including  prior  knowledge  about  the  distribution  of  the  fields likely to be
    encountered  by the correction algorithm. For example, if it is known that there is
    little  or  no  intensity  non-uniformity,  then  it  would  be  wise to penalise large
    values  for  the  intensity  nonuniformity  parameters.  This  regularisation can be
    placed  within  a  Bayesian  context,  whereby the penalty incurred is the negative
    logarithm of a prior probability for any particular pattern of nonuniformity.
    """
    self.bias_regularisation = 1e-05
    
  def setBiasRegularisationToVeryHeavy(self):
    """
    We  know  a  priori that intensity variations due to MR physics tend to be spatially
    smooth,  whereas  those  due  to different tissue types tend to contain more high
    frequency  information.  A  more accurate estimate of a bias field can be obtained
    by  including  prior  knowledge  about  the  distribution  of  the  fields likely to be
    encountered  by the correction algorithm. For example, if it is known that there is
    little  or  no  intensity  non-uniformity,  then  it  would  be  wise to penalise large
    values  for  the  intensity  nonuniformity  parameters.  This  regularisation can be
    placed  within  a  Bayesian  context,  whereby the penalty incurred is the negative
    logarithm of a prior probability for any particular pattern of nonuniformity.
    """
    self.bias_regularisation = 0.0001
    
  def setBiasRegularisationToExtremelyHeavy(self):
    """
    We  know  a  priori that intensity variations due to MR physics tend to be spatially
    smooth,  whereas  those  due  to different tissue types tend to contain more high
    frequency  information.  A  more accurate estimate of a bias field can be obtained
    by  including  prior  knowledge  about  the  distribution  of  the  fields likely to be
    encountered  by the correction algorithm. For example, if it is known that there is
    little  or  no  intensity  non-uniformity,  then  it  would  be  wise to penalise large
    values  for  the  intensity  nonuniformity  parameters.  This  regularisation can be
    placed  within  a  Bayesian  context,  whereby the penalty incurred is the negative
    logarithm of a prior probability for any particular pattern of nonuniformity.
    """
    self.bias_regularisation = 0.001
    
  def unsetBiasRegularisation(self):
    """
    We  know  a  priori that intensity variations due to MR physics tend to be spatially
    smooth,  whereas  those  due  to different tissue types tend to contain more high
    frequency  information.  A  more accurate estimate of a bias field can be obtained
    by  including  prior  knowledge  about  the  distribution  of  the  fields likely to be
    encountered  by the correction algorithm. For example, if it is known that there is
    little  or  no  intensity  non-uniformity,  then  it  would  be  wise to penalise large
    values  for  the  intensity  nonuniformity  parameters.  This  regularisation can be
    placed  within  a  Bayesian  context,  whereby the penalty incurred is the negative
    logarithm of a prior probability for any particular pattern of nonuniformity.
    """
    self.bias_regularisation = 0

  def setLMRegularisationToExtremelyLight(self):
    """
    Levenberg-Marquardt  regularisation keeps the bias correction part stable. Higher
    values means more stability, but slower convergence.
    """
    self.LM_regularisation = 1e-09
    
  def setLMRegularisationToVeryLight(self):
    """
    Levenberg-Marquardt  regularisation keeps the bias correction part stable. Higher
    values means more stability, but slower convergence.
    """
    self.LM_regularisation = 1e-08
    
  def setLMRegularisationToLight(self):
    """
    Levenberg-Marquardt  regularisation keeps the bias correction part stable. Higher
    values means more stability, but slower convergence.
    """
    self.LM_regularisation = 1e-07
    
  def setLMRegularisationToMedium(self):
    """
    Levenberg-Marquardt  regularisation keeps the bias correction part stable. Higher
    values means more stability, but slower convergence.
    """
    self.LM_regularisation = 1e-06
    
  def setLMRegularisationToHeavy(self):
    """
    Levenberg-Marquardt  regularisation keeps the bias correction part stable. Higher
    values means more stability, but slower convergence.
    """
    self.LM_regularisation = 1e-05
    
  def setLMRegularisationToVeryHeavy(self):
    """
    Levenberg-Marquardt  regularisation keeps the bias correction part stable. Higher
    values means more stability, but slower convergence.
    """
    self.LM_regularisation = 0.0001
    
  def setLMRegularisationToExtremelyHeavy(self):
    """
    Levenberg-Marquardt  regularisation keeps the bias correction part stable. Higher
    values means more stability, but slower convergence.
    """
    self.LM_regularisation = 0.001
    
  def unsetLMRegularisation(self):
    """
    Levenberg-Marquardt  regularisation keeps the bias correction part stable. Higher
    values means more stability, but slower convergence.
    """
    self.LM_regularisation = 0
    
  def getStringListForBatch(self):
    batch_list = []
    batch_list.append("bias_opts.nits = %i;" % self.iteration)
    batch_list.append("bias_opts.fwhm = %s;" % self.bias_fwhm)
    batch_list.append("bias_opts.reg = %g;" % self.bias_regularisation)
    batch_list.append("bias_opts.lmreg = %g;" % self.LM_regularisation)
    return batch_list