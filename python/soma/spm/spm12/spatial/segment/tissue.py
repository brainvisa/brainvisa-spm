# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.spatial.new_segment.tissue import Tissue as Tissue_virtual

class Tissue(Tissue_virtual):
  def __init__(self):
    self.tissue_probility_map_path = None
    self.tissue_probility_map_dimension_number = 1
    self.gaussian_number = 'Inf'
    self.native_tissue = [1, 0]
    self.warped_tissue = [0, 0]

    self.native_tissue_prefix = 'c'
    self.dartel_tissue_prefix = 'rc'
    self.warped_unmodulated_tissue_prefix = 'wc'
    self.warped_modulated_tissue_prefix = 'mwc'

    self.native_tissue_path_list = []
    self.dartel_tissue_path_list = []
    self.warped_unmodulated_tissue_path_list = []
    self.warped_modulated_tissue_path_list = []

    self._SPM_output_prefix = None#changing it is forbidden by user, only TissueContainer change it
