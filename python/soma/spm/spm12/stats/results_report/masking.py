# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.stats.results_report.masking import Masking as Masking_virtual
from soma.spm.spm_batch_maker_utils import convertPathListToSPMBatchString

class Masking():
  """Results report - Masking - SPM12"""


class Contrast(Masking, Masking_virtual):#Same as Masking in spm8
  """Masking using contrast"""
  def __init__(self):
    self.contrast_index_list = None
    self.mask_threshold_value = 0.05
    self.mask_nature = None

  def getStringListForBatch( self ):
    if not None in [self.contrast_index_list, self.mask_nature]:
      if len(self.contrast_index_list) == 1:
        contrast_str = str(self.contrast_index_list[0])
      else:
        contrast_str_list = [str(contrast) for contrast in self.contrast_index_list]
        contrast_str = '[' + ' '.join(contrast_str_list) + ']'
      batch_list = []
      batch_list.append("mask.contrast.contrasts = %s;" % contrast_str)
      batch_list.append("mask.contrast.thresh = %g;" % self.mask_threshold_value)
      batch_list.append("mask.contrast.mtype = %i;" % self.mask_nature)
      return batch_list
    else:
      raise ValueError('Unvalid contrast query masking, contrast index list and/or mask nature not found')


class Image(Masking):
  """Masking using image(s)."""
  def __init__(self):
    self.mask_images_path_list = None
    self.nature_of_mask = None

  def setMaskImagesPathList(self, path_list):
    self.mask_images_path_list = path_list

  def setNatureOfMaskToInclusive(self):
    self.nature_of_mask = 0

  def setNatureOfMaskToExclusive(self):
    self.nature_of_mask = 1

  def getStringListForBatch( self ):
    if not None in [self.mask_images_path_list, self.nature_of_mask]:
      batch_list = []
      batch_list.append("mask.image.name = %s;" % convertPathListToSPMBatchString(self.mask_images_path_list))
      batch_list.append("mask.image.mtype = %i;" % self.nature_of_mask)
      return batch_list
    else:
      raise ValueError('mask_images_path_list and nature_of_mask are requried')


