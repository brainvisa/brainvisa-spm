 # -*- coding: utf-8 -*-
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

class SubjectContainer():
  """
  Specify pairs of images to match together.
  """   
  def getStringListForBatch( self ):
    batch_list = []
    if len(self) > 1:
      for subject_index, subject in enumerate(self):
        batch_list.extend(addBatchKeyWordInEachItem("data(%s)" % (subject_index+1), subject.getStringListForBatch()))
    elif len(self) == 1:
      batch_list.extend(addBatchKeyWordInEachItem("data", self[0].getStringListForBatch()))
    else:
      raise ValueError("At least one subject is required")
    return batch_list
  
  def movePathsIfNeeded(self):
    for subject in self:
      subject.movePathsIfNeeded()