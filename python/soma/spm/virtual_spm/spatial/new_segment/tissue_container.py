# -*- coding: utf-8 -*-

from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

class TissueContainer():
  """
  The data for each subject are classified into a number of different tissue types.  The tissue
  types  are  defined  according to tissue probability maps, which define the prior probability
  of  finding  a  tissue  type  at  a  particular  location.  Typically,  the  order of tissues is grey
  matter,    white    matter,    CSF,    bone,    soft    tissue    and   air/background   (if   using
  toolbox/Seg/TPM.nii).
  """
  @checkIfArgumentTypeIsAllowed(list, 1)
  def moveTissuesIfNeeded(self, volume_path_list):
    for tissue in self:
      tissue.moveIfNeeded(volume_path_list)

  def getStringListForBatch( self ):
    batch_list = []
    if len(self) == 0:
      batch_list = ["tissue = struct('tpm', {}, 'ngaus', {}, 'native', {}, 'warped', {});"]
    elif len(self) == 1:
      batch_list.extend(addBatchKeyWordInEachItem('tissue', self[0].getStringListForBatch()))
      self.setTissueIndex(1)
    else:
      for tissue_index, tissue in enumerate(self):
        spm_index = tissue_index + 1
        key_word_tissue =  'tissue' + '(' + str(spm_index) + ')'
        batch_list.extend(addBatchKeyWordInEachItem(key_word_tissue, tissue.getStringListForBatch()))
        tissue.setTissueIndex(spm_index)
    return batch_list

