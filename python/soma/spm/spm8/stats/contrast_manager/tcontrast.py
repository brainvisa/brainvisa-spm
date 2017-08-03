# -*- coding: utf-8 -*-
from soma.spm.spm8.stats.contrast_manager.contrast import Contrast
from soma.spm.virtual_spm.stats.contrast_manager.tcontrast import TContrast as TContrast_virtual

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
