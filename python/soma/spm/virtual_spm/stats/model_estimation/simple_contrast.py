# -*- coding: utf-8 -*-
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode

class SimpleContrast():
  """
  'Simple'  contrasts refers to a contrast that spans one-dimension ie. to assess an
   effect that is increasing or decreasing.
   If  you  have  a factoral design then the contrasts needed to generate the contrast
   images  for a 2nd-level ANOVA (or to assess these simple effects within-subject)
   can be specified automatically using the ANOVA->Second level option.
   When  using the Bayesian estimation option it is computationally more efficient to
   compute  the  contrasts  when  the  parameters  are  estimated.  This  is because
   estimated   parameter   vectors  have  potentially  different  posterior  covariance
   matrices  at  different  voxels  and  these matrices are not stored. If you compute
   contrasts   post-hoc   these   matrices   must  be  recomputed  (an  approximate
   reconstruction   based  on  a  Taylor  series  expansion  is  used).  It  is  therefore
   recommended  to  specify  as  many  contrasts  as  possible  prior  to  parameter
   estimation.
   If you wish to use these contrast images for a second-level analysis then you will
   need  to  spatially smooth them to take into account between-subject differences
   in  functional  anatomy  ie.  the  fact  that  one  persons  V5 may be in a different
   position than anothers.
  """
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setName(self, name):
    self.name = name

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setVector(self, vector):
    """
    These  contrasts  are  used  to  generate  PPMs  which characterise effect sizes at
    each voxel. This is in contrast to SPMs in which eg. maps of t-statistics show the
    ratio   of   the  effect  size  to  effect  variability  (standard  deviation).  SPMs  are
    therefore  a-dimensional. This is not the case for PPMs as the size of the effect is
    of  primary  interest.  Some care is therefore needed about the scaling of contrast
    vectors.  For example, if you are interested in the differential effect size averaged
    over  conditions  then the contrast 0.5 0.5 -0.5 -0.5 would be more suitable than
    the  1  1  -1  -1  contrast which looks at the differential effect size summed over
    conditions.
    """
    self.vector = vector
  
  def getStringListForBatch( self ):
    if not None in [self.name, self.vector]:
      batch_list = ["name = '%s';" % self.name]
      vector_str_list = [str(coeff) for coeff in self.vector]
      vector_str = '\n'.join(vector_str_list)
      batch_list.append("convec = [%s];" % vector_str)
      return batch_list
    else:
      raise ValueError('Unvalid simple contrast, name and/or vector not found')
