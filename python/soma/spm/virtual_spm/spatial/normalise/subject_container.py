 # -*- coding: utf-8 -*-
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

class SubjectContainer():
  """
  List of subjects. Images of each subject should be warped differently.
  """
  def getStringListForBatch( self ):
    batch_list = []
    if len(self) > 1:
      for subject_index, subject in enumerate(self):
        batch_list.extend(addBatchKeyWordInEachItem("subj(%s)" % (subject_index+1), subject.getStringListForBatch()))
    elif len(self) == 1:
      batch_list.extend(addBatchKeyWordInEachItem("subj", self[0].getStringListForBatch()))
    else:
      raise ValueError("At least one subject is required")
    return batch_list

  def movePathsIfNeeded(self, prefix=None):
    for subject in self:
      if prefix is not None:
        subject.movePathsIfNeeded(prefix)
      else:
        subject.movePathsIfNeeded()