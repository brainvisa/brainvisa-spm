# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.tools.hdw.subject_container import SubjectContainer
from soma.spm.virtual_spm.tools.hdw.bias_correction_options import BiasCorrectionOptions
from soma.spm.virtual_spm.tools.hdw.warping_options import WarpingOptions
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem


class HDW(object):
  """
  This  toolbox  is  a  Bayesian  method  for  three dimensional registration of brain
  images.  A  finite  element  approach  is  used  to  obtain a maximum a posteriori
  (MAP) estimate of the deformation field at every voxel of a template volume.  The
  priors  used  by  the  MAP  estimate  penalize unlikely deformations and enforce a
  continuous  one-to-one  mapping.   The deformations are assumed to have some
  form  of  symmetry,  in  that  priors  describing the probability distribution of the
  deformations  should  be  identical to those for the inverses (i.e., warping brain A
  to  brain  B  should  not  be  different  probablistically  from  warping  B  to A).  A
  gradient descent algorithm is used to estimate the optimum deformations.
  Deformation  fields are written with the same name as the moved image, but with
  "y_"  prefixed  on  to  the filename.  Jacobian determinant images are also written
  (prefixed by "jy_").
  """
  def appendSubject(self, subject):
    self.subject_container.append(subject)
    
  @checkIfArgumentTypeIsAllowed(BiasCorrectionOptions, 1)  
  def replaceBiasCorrectionOptions(self, bias_correction_options):
    self.bias_correction_options = bias_correction_options
    
  @checkIfArgumentTypeIsAllowed(WarpingOptions, 1)  
  def replaceWarpingOptions(self, warping_options):
    self.warping_options = warping_options

  def getStringListForBatch( self ):
    batch_list = []
    batch_list.extend(addBatchKeyWordInEachItem("spm.tools.hdw", self.subject_container.getStringListForBatch()))
    batch_list.extend(addBatchKeyWordInEachItem("spm.tools.hdw", self.bias_correction_options.getStringListForBatch()))
    batch_list.extend(addBatchKeyWordInEachItem("spm.tools.hdw", self.warping_options.getStringListForBatch()))
    return batch_list
    
  def _moveSPMDefaultPathsIfNeeded(self):
    self.subject_container.movePathsIfNeeded()
      
      
    
    
