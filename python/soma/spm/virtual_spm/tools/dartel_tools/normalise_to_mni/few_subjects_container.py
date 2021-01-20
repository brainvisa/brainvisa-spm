# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

class FewSubjectsContainer(object):

  def getStringListForBatch( self ):
    batch_list = []
    if len(self) == 0:
      raise ValueError('At least one Subject is mandatory')
    elif len(self) == 1:
      batch_list.extend(addBatchKeyWordInEachItem('data.subj', self[0].getStringListForBatch()))
    else:
      for subject_index, subject in enumerate(self):
        key_word_subject =  'data.subj' + '(' + str(subject_index + 1) + ')'
        batch_list.extend(addBatchKeyWordInEachItem(key_word_subject, subject.getStringListForBatch()))
    return batch_list

  def moveSPMDefaultPathsIfNeeded(self):
    for subject in self:
        subject.moveSPMDefaultPathsIfNeeded()