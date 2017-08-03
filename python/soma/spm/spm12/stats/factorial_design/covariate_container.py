# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.stats.factorial_design.covariate_container import CovariateContainer as CovariateContainer_virtual
from soma.spm.spm12.stats.factorial_design.covariate import Covariate
from soma.spm.spm_container import SPMContainer

class CovariateContainer(CovariateContainer_virtual, SPMContainer):
  def __init__(self):
    SPMContainer.__init__(self, Covariate)
