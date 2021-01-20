# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.stats.model_estimation.simple_contrast_container import SimpleContrastContainer as SimpleContrastContainer_virtual
from soma.spm.spm12.stats.model_estimation.simple_contrast import SimpleContrast

from soma.spm.spm_container import SPMContainer

class SimpleContrastContainer(SimpleContrastContainer_virtual, SPMContainer):
  def __init__(self):
    SPMContainer.__init__(self, SimpleContrast)
