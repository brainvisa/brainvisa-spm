# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.spatial.normalise import Estimate as Estimate_virtual
from soma.spm.virtual_spm.spatial.normalise import Write as Write_virtual
from soma.spm.virtual_spm.spatial.normalise import EstimateAndWrite as EstimateAndWrite_virtual
from soma.spm.spm8.spatial.normalise.subject_container import SubjectContainer
from soma.spm.spm8.spatial.normalise.estimation_options import EstimationOptions
from soma.spm.spm8.spatial.normalise.writing_options import WritingOptions

from soma.spm.spm_main_module import SPM8MainModule

class Estimate(Estimate_virtual, SPM8MainModule):
  def __init__(self):
    self.subject_container = SubjectContainer()
    self.estimation_options = EstimationOptions()
#===============================================================================
#
#===============================================================================
class Write(Write_virtual, SPM8MainModule):
  def __init__(self):
    self.subject_container = SubjectContainer()
    self.writing_options = WritingOptions()
#===============================================================================
#
#===============================================================================
class EstimateAndWrite(EstimateAndWrite_virtual, SPM8MainModule):
  def __init__(self):
    self.subject_container = SubjectContainer()
    self.estimation_options = EstimationOptions()
    self.writing_options = WritingOptions()
