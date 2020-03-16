# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm8.stats.contrast_manager.contrast import Contrast
from soma.spm.virtual_spm.stats.contrast_manager.tcontrast_condsessbased import TContrastCondSessBased as TContrastCondSessBased_virtual
from soma.spm.virtual_spm.stats.contrast_manager.tcontrast_condsessbased import TContrastCondSessBasedWithExtraRegressors as TContrastCondSessBasedWithExtraRegressors_virtual
from soma.spm.virtual_spm.stats.contrast_manager.tcontrast_condsessbased import TContrastCondSessBasedWithConditions as TContrastCondSessBasedWithConditions_virtual
from soma.spm.virtual_spm.stats.contrast_manager.tcontrast_condsessbased import ContrastEntry as ContrastEntry_virtual
from soma.spm.virtual_spm.stats.contrast_manager.tcontrast_condsessbased import ContrastEntryContainer as ContrastEntryContainer_virtual

class TContrastCondSessBased(TContrastCondSessBased_virtual, Contrast):
  def __init__(self):
    self.session_vector = None
#==============================================================================
#
#==============================================================================
class TContrastCondSessBasedWithExtraRegressors(TContrastCondSessBased, TContrastCondSessBasedWithExtraRegressors_virtual):
  def __init__(self):
    TContrastCondSessBased.__init__(self)
    self.vector = []
#==============================================================================
class TContrastCondSessBasedWithConditions(TContrastCondSessBased, TContrastCondSessBasedWithConditions_virtual):
  def __init__(self):
    TContrastCondSessBased.__init__(self)
    self.contrast_entry_container = ContrastEntryContainer()
#==============================================================================
class ContrastEntry(ContrastEntry_virtual):
  def __init__(self):
    self.contrast_weight = None
    self.condition = None
    self.basis_function = None
    self.parametric_modulation = None
    self.parametric_modulation_order = None
#==============================================================================
class ContrastEntryContainer(ContrastEntryContainer_virtual):
  def __init__(self):
    self.contrast_entry_list = []
