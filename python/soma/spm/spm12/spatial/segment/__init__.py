 # -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.spatial.new_segment import NewSegment as NewSegment_virtual
from soma.spm.spm_main_module import SPM12MainModule

from soma.spm.spm12.spatial.segment.channel_container import ChannelContainer
from soma.spm.spm12.spatial.segment.channel import Channel
from soma.spm.spm12.spatial.segment.tissue_container import TissueContainer
from soma.spm.spm12.spatial.segment.tissue import Tissue

from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem, convertlistToSPMString
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode

import numbers

class Segment(NewSegment_virtual, SPM12MainModule):
  def __init__(self):
    self.channel_container = ChannelContainer()
    self.tissue_container = TissueContainer()
    self.MRF_parameter = 1.0
    self.clean_up = 1
    self.warping_regularisation = [0, 0.001, 0.5, 0.05, 0.2]
    self.affine_regularisation = 'mni'
    self.smoothness = 0
    self.sampling_distance = 3.0
    self.deformation_fields = [0, 0]

    self.forward_deformation_prefix = 'y_'
    self.inverse_deformation_prefix = 'iy_'

    self.forward_deformation_path_list = []
    self.inverse_deformation_path_list = []
    self.seg8_mat_path_list = []

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setSPMDefaultChannel(self, volume_path_list):
    default_channel = Channel()
    default_channel.setVolumePathList(volume_path_list)
    self.channel_container.clear()
    self.channel_container.append(default_channel)

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setSPMDefautTissues(self, tissue_proba_map_path):
    self.tissue_container.clear()

    first_tissue = Tissue()
    first_tissue.setTissueProbilityMapPath(tissue_proba_map_path)
    first_tissue.setTissueProbilityDimension(1)
    first_tissue.setGaussianNumber(1)
    first_tissue.setNativeTissueNativeSpace()
    first_tissue.unsetWarpedTissue()
    self.tissue_container.append(first_tissue)

    second_tissue = Tissue()
    second_tissue.setTissueProbilityMapPath(tissue_proba_map_path)
    second_tissue.setTissueProbilityDimension(2)
    second_tissue.setGaussianNumber(1)
    second_tissue.setNativeTissueNativeSpace()
    second_tissue.unsetWarpedTissue()
    self.tissue_container.append(second_tissue)

    third_tissue = Tissue()
    third_tissue.setTissueProbilityMapPath(tissue_proba_map_path)
    third_tissue.setTissueProbilityDimension(3)
    third_tissue.setGaussianNumber(2)
    third_tissue.setNativeTissueNativeSpace()
    third_tissue.unsetWarpedTissue()
    self.tissue_container.append(third_tissue)

    fourth_tissue = Tissue()
    fourth_tissue.setTissueProbilityMapPath(tissue_proba_map_path)
    fourth_tissue.setTissueProbilityDimension(4)
    fourth_tissue.setGaussianNumber(3)
    fourth_tissue.setNativeTissueNativeSpace()
    fourth_tissue.unsetWarpedTissue()
    self.tissue_container.append(fourth_tissue)

    fifth_tissue = Tissue()
    fifth_tissue.setTissueProbilityMapPath(tissue_proba_map_path)
    fifth_tissue.setTissueProbilityDimension(5)
    fifth_tissue.setGaussianNumber(4)
    fifth_tissue.setNativeTissueNativeSpace()
    fifth_tissue.unsetWarpedTissue()
    self.tissue_container.append(fifth_tissue)

    sixth_tissue = Tissue()
    sixth_tissue.setTissueProbilityMapPath(tissue_proba_map_path)
    sixth_tissue.setTissueProbilityDimension(6)
    sixth_tissue.setGaussianNumber(2)
    sixth_tissue.unsetNativeTissue()
    sixth_tissue.unsetWarpedTissue()
    self.tissue_container.append(sixth_tissue)

  def setCleanUpToLight(self):
    self.clean_up = 1

  def setCleanUpToThorough(self):
    self.clean_up = 2

  def unsetCleanUp(self):
    self.clean_up = 0

  @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
  def setSmoothness(self, smoothness_factor):
    self.smoothness = smoothness_factor

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setWarpingRegularisation(self, regularisation_list):
    if len(regularisation_list) == 5:
      self.warping_regularisation = regularisation_list
    else:
      raise ValueError('Warping regularisation value must be list of 5 numbers')

  def getStringListForBatch(self):
    batch_list = []
    batch_list.extend(self.channel_container.getStringListForBatch())
    batch_list.extend(self.tissue_container.getStringListForBatch())
    batch_list.append('warp.mrf = ' + str(self.MRF_parameter) + ';')
    batch_list.append('warp.cleanup = ' + str(self.clean_up) + ';')
    batch_list.append('warp.reg = ' + convertlistToSPMString(self.warping_regularisation) + ';')
    batch_list.append("warp.affreg = '" + str(self.affine_regularisation) + "';")
    batch_list.append('warp.fwhm = ' + str(self.smoothness) + ';')
    batch_list.append('warp.samp = ' + str(self.sampling_distance) + ';')
    batch_list.append('warp.write = ' + str(self.deformation_fields) + ';')
    return self._addSpecificSPMPrefix(batch_list)

  def _addSpecificSPMPrefix(self, batch_list):
    spm8_keyword = 'spm.spatial.preproc'
    return addBatchKeyWordInEachItem(spm8_keyword, batch_list)




