 # -*- coding: utf-8 -*-
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.virtual_spm.spatial.normalise.estimation_options import EstimationOptions
from soma.spm.virtual_spm.spatial.normalise.writing_options import WritingOptions

class Normalise():
  def appendSubject(self, subject):
    self.subject_container.append(subject)

  def clearSubjectList(self, subject):
    self.subject_container.clear()
#===============================================================================
#
#===============================================================================
class Estimate(Normalise):
  """
  Computes  the  warp  that  best  registers  a  source  image  (or  series of source
  images) to match a template, saving it to a file image name'_sn.mat'.
  """
  @checkIfArgumentTypeIsAllowed(EstimationOptions, 1)
  def replaceEstimateOptions(self, estimation_options):
    del self.estimation_options
    self.estimation_options = estimation_options

  def getStringListForBatch(self):
    batch_list = []
    batch_list.extend(addBatchKeyWordInEachItem("spm.spatial.normalise.est", self.subject_container.getStringListForBatch()))
    batch_list.extend(addBatchKeyWordInEachItem("spm.spatial.normalise.est", self.estimation_options.getStringListForBatch()))
    return batch_list

  def _moveSPMDefaultPathsIfNeeded(self):
    self.subject_container.movePathsIfNeeded()
#===============================================================================
#
#===============================================================================
class Write(Normalise):
  """
  Computes  the  warp  that  best  registers  a  source  image  (or  series of source
  images) to match a template, saving it to a file image name'_sn.mat'.
  """
  @checkIfArgumentTypeIsAllowed(WritingOptions, 1)
  def replaceWrintingOptions(self, writing_options):
    del self.writing_options
    self.writing_options = writing_options

  def getStringListForBatch(self):
    batch_list = []
    batch_list.extend(addBatchKeyWordInEachItem("spm.spatial.normalise.write", self.subject_container.getStringListForBatch()))
    batch_list.extend(addBatchKeyWordInEachItem("spm.spatial.normalise.write", self.writing_options.getStringListForBatch()))
    return batch_list

  def _moveSPMDefaultPathsIfNeeded(self):
    prefix = self.writing_options.getCurrentFilenamePrefix()
    self.subject_container.movePathsIfNeeded(prefix)
#===============================================================================
#
#===============================================================================
class EstimateAndWrite(Estimate, Write):
  """
  Computes  the  warp  that  best  registers  a  source  image  (or  series of source
  images)  to  match  a  template,  saving  it  to  the  file image name'_sn.mat'. This
  option also allows the contents of the image name'_sn.mat' files to be applied to a
  series of images.
  """
  def getStringListForBatch(self):
    batch_list = []
    batch_list.extend(addBatchKeyWordInEachItem("spm.spatial.normalise.estwrite", self.subject_container.getStringListForBatch()))
    batch_list.extend(addBatchKeyWordInEachItem("spm.spatial.normalise.estwrite", self.estimation_options.getStringListForBatch()))
    batch_list.extend(addBatchKeyWordInEachItem("spm.spatial.normalise.estwrite", self.writing_options.getStringListForBatch()))
    return batch_list

  def _moveSPMDefaultPathsIfNeeded(self):
    prefix = self.writing_options.getCurrentFilenamePrefix()
    self.subject_container.movePathsIfNeeded(prefix)
