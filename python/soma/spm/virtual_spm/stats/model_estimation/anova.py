# -*- coding: utf-8 -*-
class ANOVA():
  """
  Perform 1st or 2nd level Analysis of Variance.
  """
  def enableFirstLevel(self):
    """
    This  is  implemented  using Bayesian model comparison. For example, to test for
    the  main  effect  of  a  factor two models are compared, one where the levels are
    represented  using  different  regressors  and  one using the same regressor. This
    therefore   requires   explicit   fitting   of  several  models  at  each  voxel  and  is
    computationally   demanding   (requiring   several   hours   of  computation).  The
    recommended option is therefore NO.
    """
    self.first_level = 'Yes'

  def disableFirstLevel(self):
    self.first_level = 'No'

  def enableSecondLevel(self):
    """
    This  option  tells  SPM  to  automatically  generate  the  simple contrasts that are
    necessary  to  produce  the contrast images for a second-level (between-subject)
    ANOVA. Naturally, these contrasts can also be used to characterise simple effects
    for each subject.
    With   the   Bayesian  estimation  option  it  is  recommended  that  contrasts  are
    computed  during  the  parameter estimation stage (see 'simple contrasts' below).
    The recommended option here is therefore YES.
    To  use  this  option  you must have already specified your factorial design during
    the model specification stage.
    If you wish to use these contrast images for a second-level analysis then you will
    need  to  spatially smooth them to take into account between-subject differences
    in  functional  anatomy  ie.  the  fact  that  one  persons  V5 may be in a different
    position than anothers.
    
    """
    self.second_level = 'Yes'

  def disableSecondLevel(self):
    self.second_level = 'No'
  
  def getStringListForBatch( self ):
    batch_list = ["anova.first = '%s'" % self.first_level]
    batch_list.append("anova.second = '%s';" % self.second_level)
    return batch_list
