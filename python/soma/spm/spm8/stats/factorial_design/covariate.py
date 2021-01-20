# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.stats.factorial_design.covariate import Covariate as Covariate_virtual

class Covariate(Covariate_virtual):
  def __init__(self):
    self.possible_interaction_dict = {'None':1, 'With Factor 1':2 , 'With Factor 2':3, 'With Factor 3':4}
    self.possible_centering_dict = {'Overall mean':1,
                                    'Factor 1 mean':2,
                                    'Factor 2 mean':3,
                                    'Factor 3 mean':4,
                                    'No centering':5,
                                    'User specified value':6,
                                    'As implied by ANCOVA':7,
                                    'GM':8}
    self.vector = None
    self.name = None
    self.interactions = 'None'
    self.centering = 'Overall mean'
