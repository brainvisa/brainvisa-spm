# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.stats.contrast_manager.contrast_container import ContrastContainer as ContrastContainer_virtual
from soma.spm.spm8.stats.contrast_manager.contrast import Contrast
from soma.spm.spm_container import SPMContainer

class ContrastContainer(ContrastContainer_virtual, SPMContainer):
  def __init__(self):
    SPMContainer.__init__(self, Contrast)
