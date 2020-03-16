# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm12.stats.contrast_manager.contrast import Contrast
from soma.spm.virtual_spm.stats.contrast_manager.tcontrast import TContrast as TContrast_virtual

from soma.spm.spm_batch_maker_utils import convertlistToSPMString

class TContrast(TContrast_virtual, Contrast):
  def __init__(self):
    self.possible_options = {"Do not replicate":'none',
                             'Replicate':'repl',
                             'Replicate and Scale':'replsc',
                             'Create per session':'sess',
                             'Replicate and Create per session':'both',
                             'Replicate and Scale and Create per session':'bothsc',
                             }
    self.replicate_over_sessions = 'none'
    self.vector = []

  def getStringListForBatch( self ):
    if not None in [self.vector, self.name]:
      batch_list = []
      batch_list.append("tcon.name = '%s';" % self.name)
      batch_list.append("tcon.weights = %s;" % convertlistToSPMString(self.vector))
      batch_list.append("tcon.sessrep = '%s';" % self.replicate_over_sessions)
      return batch_list
    else:
      raise ValueError('Unvalid contrast, name or vector not found')
