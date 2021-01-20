# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

class ChannelContainer(object):
  """
  Specify  the number of different channels (for multi-spectral classification). If you
  have  scans  of  different contrasts for each of the subjects, then it is possible to
  combine   the  information  from  them  in  order  to  improve  the  segmentation
  accuracy.  Note  that  only  the  first  channel  of data is used for the initial affine
  registration with the tissue probability maps.
  """
  def moveBiasSavingIfNeeded(self):
    for channel in self:
      channel.moveBiasSavingIfNeeded()

  def getStringListForBatch( self ):
    batch_list = []
    if len(self) == 0:
      raise ValueError('At least one channel is mandatory')
    elif len(self) == 1:
      batch_list.extend(addBatchKeyWordInEachItem('channel', self[0].getStringListForBatch()))
    else:
      for channel_index, channel in enumerate(self):
        key_word_channel =  'channel' + '(' + str(channel_index + 1) + ')'
        batch_list.extend(addBatchKeyWordInEachItem(key_word_channel, channel.getStringListForBatch()))
    return batch_list
