# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.spatial.new_segment.tissue_container import TissueContainer as TissueContainer_virtual
from soma.spm.spm12.spatial.segment.tissue import Tissue

from soma.spm.spm_container import SPMContainer

class TissueContainer(TissueContainer_virtual, SPMContainer):
  def __init__(self):
    SPMContainer.__init__(self, Tissue)
