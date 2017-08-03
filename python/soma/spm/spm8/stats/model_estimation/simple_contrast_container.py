# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.stats.model_estimation.simple_contrast_container import SimpleContrastContainer as SimpleContrastContainer_virtual
from soma.spm.spm8.stats.model_estimation.simple_contrast import SimpleContrast

from soma.spm.spm_container import SPMContainer

class SimpleContrastContainer(SimpleContrastContainer_virtual, SPMContainer):
  def __init__(self):
    SPMContainer.__init__(self, SimpleContrast)
