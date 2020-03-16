# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode

class Covariate(object):
  """
  This  option  allows  for  the  specification  of  covariates  and nuisance variables.
  Unlike  SPM94/5/6,  where  the design was partitioned into effects of interest and
  nuisance  effects  for the computation of adjusted data and the F-statistic (which
  was  used to thresh out voxels where there appeared to be no effects of interest),
  SPM  does  not  partition  the  design  in  this  way  anymore.  The only remaining
  distinction  between effects of interest (including covariates) and nuisance effects
  is  their  location  in  the  design  matrix,  which we have retained for continuity. 
  """
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setVector(self, vector):
    """
    Vector of covariate values.
    Enter  the  covariate values ''per subject'' (i.e. all for subject 1, then all for subject
    2,  etc).  Importantly,  the  ordering of the cells of a factorial design has to be the
    same  for  all subjects in order to be consistent with the ordering of the covariate
    values.
    """
    self.vector = vector

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setName(self, name):
    """
    Name of covariate
    """
    self.name = name

  def setInteraction(self, interaction):
    """
    For   each  covariate  you  have  defined,  there  is  an  opportunity  to  create  an
    additional  regressor  that  is  the  interaction between the covariate and a chosen
    experimental factor.
    """
    if interaction in list(self.possible_interaction_dict.keys()):
      self.interactions = interaction
    else:
      raise ValueError('Covariates interactions possibilities are : ' + str(list(self.possible_interaction_dict.keys())))

  def setCentering(self, centering):
    """
    The  appropriate  centering  option  is  usually  the  one  that  corresponds to the
    interaction  chosen,  and ensures that main effects of the interacting factor aren't
    affected  by the covariate. You are advised to choose this option, unless you have
    other modelling considerations.
    """
    if centering in list(self.possible_centering_dict.keys()):
      self.centering = centering
    else:
      raise ValueError('Covariates centering possibilities are : ' + str(list(self.possible_centering_dict.keys())))
 
  def getStringListForBatch(self):
    if not None in [self.vector, self.name]:
      vector_list = [str(coeff) for coeff in self.vector]
      vector_str = '\n'.join(vector_list)
      batch_list = []
      batch_list.append("c = [%s];" % vector_str)
      batch_list.append("cname = '%s';" % self.name)
      batch_list.append("iCFI = %s;" % self.possible_interaction_dict[self.interactions])
      batch_list.append("iCC = %s;" % self.possible_centering_dict[self.centering])
      return batch_list
    else:
      raise ValueError('Unvalid covariate, name or vector not found')
    
