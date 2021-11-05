# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
from soma.spm.virtual_spm.spatial.normalise import Estimate as Estimate_virtual
from soma.spm.virtual_spm.spatial.normalise import Write as Write_virtual
from soma.spm.virtual_spm.spatial.normalise import EstimateAndWrite as EstimateAndWrite_virtual
from soma.spm.spm12.spatial.old_normalise.subject_container import SubjectContainer
from soma.spm.spm12.spatial.old_normalise.estimation_options import EstimationOptions
from soma.spm.spm12.spatial.old_normalise.writing_options import WritingOptions

from soma.spm.spm_main_module import SPM12MainModule

class Estimate(Estimate_virtual, SPM12MainModule):
  def __init__(self):
    self.subject_container = SubjectContainer()
    self.estimation_options = EstimationOptions()

  def getStringListForBatch(self):
    batch_list = []
    batch_list.extend(addBatchKeyWordInEachItem("spm.tools.oldnorm.est", self.subject_container.getStringListForBatch()))
    batch_list.extend(addBatchKeyWordInEachItem("spm.tools.oldnorm.est", self.estimation_options.getStringListForBatch()))
    return batch_list
#===============================================================================
#
#===============================================================================
class Write(Write_virtual, SPM12MainModule):
  def __init__(self):
    self.subject_container = SubjectContainer()
    self.writing_options = WritingOptions()

  def getStringListForBatch(self):
    batch_list = []
    batch_list.extend(addBatchKeyWordInEachItem("spm.tools.oldnorm.write", self.subject_container.getStringListForBatch()))
    batch_list.extend(addBatchKeyWordInEachItem("spm.tools.oldnorm.write", self.writing_options.getStringListForBatch()))
    return batch_list
#===============================================================================
#
#===============================================================================
class EstimateAndWrite(EstimateAndWrite_virtual, SPM12MainModule):
  def __init__(self):
    self.subject_container = SubjectContainer()
    self.estimation_options = EstimationOptions()
    self.writing_options = WritingOptions()

  def getStringListForBatch(self):
    batch_list = []
    batch_list.extend(addBatchKeyWordInEachItem("spm.tools.oldnorm.estwrite", self.subject_container.getStringListForBatch()))
    batch_list.extend(addBatchKeyWordInEachItem("spm.tools.oldnorm.estwrite", self.estimation_options.getStringListForBatch()))
    batch_list.extend(addBatchKeyWordInEachItem("spm.tools.oldnorm.estwrite", self.writing_options.getStringListForBatch()))
    return batch_list
