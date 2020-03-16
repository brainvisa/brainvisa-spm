# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed

class TwoSampleTTestDesign(object):
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setGroup1Scans(self, scans):
    self.group_1_scans = scans

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setGroup2Scans(self, scans):
    self.group_2_scans = scans

  def enableIndependence(self):
    """
    By default, the measurements are assumed to be independent between levels. 
    If   you   change   this  option  to  allow  for  dependencies,  this  will  violate  the
    assumption  of  sphericity.  It  would  therefore be an example of non-sphericity.
    One  such  example  would  be  where  you had repeated measurements from the
    same  subjects  -  it  may  then  be  the  case  that,  over  subjects, measure 1 is
    correlated to measure 2.
    Restricted  Maximum  Likelihood (REML): The ensuing covariance components will
    be  estimated  using  ReML  in  spm_spm  (assuming  the  same for all responsive
    voxels)   and   used   to  adjust  the  statistics  and  degrees  of  freedom  during
    inference.   By  default  spm_spm  will  use  weighted  least  squares  to  produce
    Gauss-Markov   or   Maximum   likelihood  estimators  using  the  non-sphericity
    structure  specified  at  this  stage. The components will be found in SPM.xVi and
    enter the estimation procedure exactly as the serial correlations in fMRI models.
    """
    self.independence = 0

  def disableIndependence(self):
    """
    By default, the measurements are assumed to be independent between levels. 
    If   you   change   this  option  to  allow  for  dependencies,  this  will  violate  the
    assumption  of  sphericity.  It  would  therefore be an example of non-sphericity.
    One  such  example  would  be  where  you had repeated measurements from the
    same  subjects  -  it  may  then  be  the  case  that,  over  subjects, measure 1 is
    correlated to measure 2.
    Restricted  Maximum  Likelihood (REML): The ensuing covariance components will
    be  estimated  using  ReML  in  spm_spm  (assuming  the  same for all responsive
    voxels)   and   used   to  adjust  the  statistics  and  degrees  of  freedom  during
    inference.   By  default  spm_spm  will  use  weighted  least  squares  to  produce
    Gauss-Markov   or   Maximum   likelihood  estimators  using  the  non-sphericity
    structure  specified  at  this  stage. The components will be found in SPM.xVi and
    enter the estimation procedure exactly as the serial correlations in fMRI models.
    """
    self.independence = 1

  def setEqualVariance(self):
    """
    By default, the measurements in each level are assumed to have unequal variance. 
    This  violates  the  assumption  of  'sphericity'  and  is  therefore  an  example  of
    'non-sphericity'.
    This can occur, for example, in a 2nd-level analysis of variance, one contrast may
    be scaled differently from another.  Another example would be the comparison of
    qualitatively  different  dependent  variables (e.g. normals vs. patients).  Different
    variances  (heteroscedasticy)  induce  different  error covariance components that
    are estimated using restricted maximum likelihood (see below).
    Restricted  Maximum  Likelihood (REML): The ensuing covariance components will
    be  estimated  using  ReML  in  spm_spm  (assuming  the  same for all responsive
    voxels)   and   used   to  adjust  the  statistics  and  degrees  of  freedom  during
    inference.   By  default  spm_spm  will  use  weighted  least  squares  to  produce
    Gauss-Markov   or   Maximum   likelihood  estimators  using  the  non-sphericity
    structure  specified  at  this  stage. The components will be found in SPM.xVi and
    enter the estimation procedure exactly as the serial correlations in fMRI models.
    """
    self.variance = 0

  def setUnequalVariance(self):
    self.variance = 1
    """
    By default, the measurements in each level are assumed to have unequal variance. 
    This  violates  the  assumption  of  'sphericity'  and  is  therefore  an  example  of
    'non-sphericity'.
    This can occur, for example, in a 2nd-level analysis of variance, one contrast may
    be scaled differently from another.  Another example would be the comparison of
    qualitatively  different  dependent  variables (e.g. normals vs. patients).  Different
    variances  (heteroscedasticy)  induce  different  error covariance components that
    are estimated using restricted maximum likelihood (see below).
    Restricted  Maximum  Likelihood (REML): The ensuing covariance components will
    be  estimated  using  ReML  in  spm_spm  (assuming  the  same for all responsive
    voxels)   and   used   to  adjust  the  statistics  and  degrees  of  freedom  during
    inference.   By  default  spm_spm  will  use  weighted  least  squares  to  produce
    Gauss-Markov   or   Maximum   likelihood  estimators  using  the  non-sphericity
    structure  specified  at  this  stage. The components will be found in SPM.xVi and
    enter the estimation procedure exactly as the serial correlations in fMRI models.
    """

  def enableGrandMeanScaling(self):
    """
    This option is only used for PET data.
    Selecting YES will specify 'grand mean scaling by factor' which could be eg. 'grand
    mean scaling by subject' if the factor is 'subject'.
    Since  differences  between  subjects  may  be due to gain and sensitivity effects,
    AnCova  by  subject  could  be  combined with "grand mean scaling by subject" to
    obtain  a  combination of between subject proportional scaling and within subject
    AnCova.
    """
    self.grand_mean_scaling = 1

  def disableGrandMeanScaling(self):
    """
    This option is only used for PET data.
    Selecting YES will specify 'grand mean scaling by factor' which could be eg. 'grand
    mean scaling by subject' if the factor is 'subject'.
    Since  differences  between  subjects  may  be due to gain and sensitivity effects,
    AnCova  by  subject  could  be  combined with "grand mean scaling by subject" to
    obtain  a  combination of between subject proportional scaling and within subject
    AnCova.
    """
    self.grand_mean_scaling = 0

  def enableANCOVA(self):
    """
    This option is only used for PET data.
    Selecting   YES  will  specify  'ANCOVA-by-factor'  regressors.  This  includes  eg.
    'Ancova  by  subject'  or  'Ancova  by  effect'.  These  options  allow  eg.  different
    subjects to have different relationships between local and global measurements.
    """
    self.ANCOVA = 1

  def disableANCOVA(self):
    """
    This option is only used for PET data.
    Selecting   YES  will  specify  'ANCOVA-by-factor'  regressors.  This  includes  eg.
    'Ancova  by  subject'  or  'Ancova  by  effect'.  These  options  allow  eg.  different
    subjects to have different relationships between local and global measurements.
    """
    self.ANCOVA = 0
  
  def getStringListForBatch( self ):
    if not None in [self.group_1_scans, self.group_2_scans]:
      batch_list = []
      batch_list.append("des.t2.scans1 = %s;" % self._buildStringAboutScansForBatch(self.group_1_scans))
      batch_list.append("des.t2.scans2 = %s;" % self._buildStringAboutScansForBatch(self.group_2_scans))
      batch_list.append("des.t2.dept = %s;" % self.independence)
      batch_list.append("des.t2.variance = %s;" % self.variance)
      batch_list.append("des.t2.gmsca = %s;" % self.grand_mean_scaling)
      batch_list.append("des.t2.ancova = %s;" % self.ANCOVA)
      return batch_list
    else:
      raise ValueError('OneSampleTTestDesign needs images list')
    
  def _buildStringAboutScansForBatch(self, scans_list):
      scans_path_list = []
      for scans in scans_list:
        scans_path_list.append("'%s,1'" % scans)
      return '{' + "\n".join(scans_path_list) + '}'
    