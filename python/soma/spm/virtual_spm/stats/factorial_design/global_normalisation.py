# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

class GlobalNormalisation(object):
  """
  This option is only used for PET data.
  Global  nuisance effects are usually accounted for either by scaling the images so
  that  they all have the same global value (proportional scaling), or by including the
  global  covariate  as  a nuisance effect in the general linear model (AnCova). Much
  has  been written on which to use, and when. Basically, since proportional scaling
  also  scales  the  variance  term,  it  is appropriate for situations where the global
  measurement   predominantly   reflects   gain  or  sensitivity.  Where  variance  is
  constant   across  the  range  of  global  values,  linear  modelling  in  an  AnCova
  approach  has  more  flexibility,  since  the  model  is  not  restricted  to a simple
  proportional regression.
  """
  def enableOverallGrandMeanScaling(self):
    """
    Scaling  of  the  overall grand mean simply scales all the data by a common factor                                    
    such  that  the  mean of all the global values is the value specified. For qualitative
    data,  this  puts  the  data  into an intuitively accessible scale without altering the
    statistics.
    """
    self.overall_grand_mean_scaling.enable()

  def setOverallGrandMeanScalingValue(self, grand_mean_scaled_value):
    """
    The default value of 50, scales the global flow to a physiologically realistic value of 50ml/dl/min.
    """
    self.overall_grand_mean_scaling.setValue(grand_mean_scaled_value)

  def disableOverallGrandMeanScaling(self):
    self.overall_grand_mean_scaling.disable()

  def unsetNormalisation( self):
    """
    Global  nuisance effects are usually accounted for either by scaling the images so
    that  they all have the same global value (proportional scaling), or by including the
    global  covariate  as  a nuisance effect in the general linear model (AnCova). Much
    has  been written on which to use, and when. Basically, since proportional scaling
    also  scales  the  variance  term,  it  is appropriate for situations where the global
    measurement   predominantly   reflects   gain  or  sensitivity.  Where  variance  is
    constant   across  the  range  of  global  values,  linear  modelling  in  an  AnCova
    approach  has  more  flexibility,  since  the  model  is  not  restricted  to a simple
    proportional regression.
    """
    self.normalisation = 1

  def setNormalisationToProportional(self):
    """
    Global  nuisance effects are usually accounted for either by scaling the images so
    that  they all have the same global value (proportional scaling), or by including the
    global  covariate  as  a nuisance effect in the general linear model (AnCova). Much
    has  been written on which to use, and when. Basically, since proportional scaling
    also  scales  the  variance  term,  it  is appropriate for situations where the global
    measurement   predominantly   reflects   gain  or  sensitivity.  Where  variance  is
    constant   across  the  range  of  global  values,  linear  modelling  in  an  AnCova
    approach  has  more  flexibility,  since  the  model  is  not  restricted  to a simple
    proportional regression.
    """
    self.normalisation = 2

  def setNormalisationToANCOVA(self):
    self.normalisation = 3
   
  def getStringListForBatch( self ):
    batch_list = []
    batch_list.extend(addBatchKeyWordInEachItem("globalm", self.overall_grand_mean_scaling.getStringListForBatch()))
    batch_list.append("globalm.glonorm = %i;" % self.normalisation)
    return batch_list


class OverallGrandMeanScaling(object):
  def enable(self):
    self.is_activate = True

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setValue(self, grand_mean_scaled_value):
    self.grand_mean_scaled_value = grand_mean_scaled_value

  def disable( self ):
    self.is_activate = False
    self.grand_mean_scaled_value = []
  
  def getStringListForBatch( self ):
    if self.is_activate:
      if len( self.grand_mean_scaled_value ) == 1:
        batch_list = ["gmsca.gmsca_yes.gmscv = %i;" % self.grand_mean_scaled_value[ 0 ]]
      elif len( self.grand_mean_scaled_value ) > 1:
        value_str = [ str( val ) for val in self.grand_mean_scaled_value ]
        grand_mean_scaled_value_str = '\n'.join( value_str )
        batch_list = ["gmsca.gmsca_yes.gmscv = [%s];" % grand_mean_scaled_value_str]
    else:
      batch_list = ["gmsca.gmsca_no = 1;"]
    return batch_list
    