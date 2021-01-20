 # -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
import numbers 

class EstimationOptions(object):
  """
  Various settings for estimating warps.
  """
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setTemplateImage(self, template_path):
    """
    Specify  a  template  image  to  match  the source image with. The contrast in the
    template  must  be  similar to that of the source image in order to achieve a good
    registration.    It  is also possible to select more than one template, in which case
    the  registration  algorithm  will  try  to  find the best linear combination of these
    images in order to best model the intensities in the source image.
    """
    self.template_path = template_path
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setTemplateWeightingImage(self, template_weighting_path):
    """
    Applies  a  weighting  mask  to  the template(s) during the parameter estimation. 
    With  the  default  brain mask, weights in and around the brain have values of one
    whereas  those  clearly  outside the brain are zero.  This is an attempt to base the
    normalisation  purely  upon  the  shape  of the brain, rather than the shape of the
    head  (since  low  frequency  basis functions can not really cope with variations in
    skull thickness).
    The option is now available for a user specified weighting image. This should have
    the  same  dimensions  and  mat  file  as  the template images, with values in the
    range of zero to one.
    """
    self.template_weighting_path = template_weighting_path
    
  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
  def setSourceImageSmoothing(self, source_image_smoothing):
    """
    Smoothing  to  apply  to  a  copy  of  the  source image. The template and source
    images  should  have  approximately  the  same  smoothness. Remember that the
    templates   supplied   with   SPM   have   been   smoothed   by   8mm,   and  that
    smoothnesses combine by Pythagoras' rule.
    """
    self.source_image_smoothing = source_image_smoothing
    
  def setTemplateImageSmoothing(self, template_image_smoothing):
    """
    Smoothing  to  apply  to  a  copy of the template image. The template and source
    images  should  have  approximately  the  same  smoothness. Remember that the
    templates   supplied   with   SPM   have   been   smoothed   by   8mm,   and  that
    smoothnesses combine by Pythagoras' rule.
    """
    self.template_image_smoothing = template_image_smoothing
    
  def setAffineRegularisationToICBMSpaceTemplate(self):
    """
    Affine   registration   into   a   standard   space   can  be  made  more  robust  by
    regularisation  (penalising  excessive  stretching or shrinking).  The best solutions
    can be obtained by knowing the approximate amount of stretching that is needed
    (e.g.  ICBM templates are slightly bigger than typical brains, so greater zooms are
    likely  to  be  needed).  If registering to an image in ICBM/MNI space, then choose
    this  option.
    """
    self.affine_regularisation = 'mni'
    
  def setAffineRegularisationToAverageSizedTemplate(self):
    """
    Affine   registration   into   a   standard   space   can  be  made  more  robust  by
    regularisation  (penalising  excessive  stretching or shrinking).  The best solutions
    can be obtained by knowing the approximate amount of stretching that is needed
    (e.g.  ICBM templates are slightly bigger than typical brains, so greater zooms are
    likely  to  be  needed).  If registering to a template that is close in size, then select this
    option.
    """
    self.affine_regularisation = 'subj'
    
  def unsetAffineRegularisation(self):
    """
    Affine   registration   into   a   standard   space   can  be  made  more  robust  by
    regularisation  (penalising  excessive  stretching or shrinking).  The best solutions
    can be obtained by knowing the approximate amount of stretching that is needed
    (e.g.  ICBM templates are slightly bigger than typical brains, so greater zooms are
    likely  to  be  needed).  If you do not want to regularise, then choose this option.
    """
    self.affine_regularisation = 'none'
    
  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
  def setNonLinearFrequencyCutOff(self, cutoff):
    """
    Cutoff  of DCT bases.  Only DCT bases of periods longer than the cutoff are used
    to describe the warps. The number used will depend on the cutoff and the field of
    view of the template image(s).
    """
    self.cutoff = cutoff
    
  @checkIfArgumentTypeIsAllowed(int, 1)
  def setNonLinearIterations(self, iterations):
    """
    Number of iterations of nonlinear warping performed.
    """
    self.iterations = iterations
    
  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
  def setNonLinearRegularisation(self, regularisation):
    """
    The  amount  of  regularisation for the nonlinear part of the spatial normalisation.
    Pick  a  value  around  one.  However, if your normalised images appear distorted,
    then  it  may  be  an  idea to increase the amount of regularisation (by an order of
    magnitude)   -   or   even  just  use  an  affine  normalisation.  The  regularisation
    influences the smoothness of the deformation fields.
    """
    self.regularisation = regularisation
    
  def getStringListForBatch(self):
    if self.template_path is not None:
      batch_list = []
      batch_list.append("eoptions.template = {'%s,1'};" %self.template_path)
      if self.template_weighting_path:
        batch_list.append("eoptions.weight = {'%s,1'};" %self.template_weighting_path)
      else:
        batch_list.append("eoptions.weight = '';")
      batch_list.append("eoptions.smosrc = %g;" %self.source_image_smoothing)
      batch_list.append("eoptions.smoref = %g;" %self.template_image_smoothing)
      batch_list.append("eoptions.regtype = '%s';" %self.affine_regularisation)
      batch_list.append("eoptions.cutoff = %g;" %self.cutoff)
      batch_list.append("eoptions.nits = %i;" %self.iterations)
      batch_list.append("eoptions.reg = %g;" %self.regularisation)
      return batch_list
    else:
      raise ValueError("template_path is required")