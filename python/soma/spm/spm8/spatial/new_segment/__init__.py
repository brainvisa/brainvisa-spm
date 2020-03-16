 # -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.spatial.new_segment import NewSegment as NewSegment_virtual
from soma.spm.spm_main_module import SPM8MainModule
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsStrOrUnicode
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed

from soma.spm.spm8.spatial.new_segment.channel_container import ChannelContainer
from soma.spm.spm8.spatial.new_segment.channel import Channel
from soma.spm.spm8.spatial.new_segment.tissue_container import TissueContainer
from soma.spm.spm8.spatial.new_segment.tissue import Tissue

class NewSegment(NewSegment_virtual, SPM8MainModule):
  def __init__(self):
    self.channel_container = ChannelContainer()
    self.tissue_container = TissueContainer()
    self.MRF_parameter = 0
    self.warping_regularisation = 4
    self.affine_regularisation = 'mni'
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
    first_tissue.setGaussianNumber(2)
    first_tissue.setNativeTissueNativeSpace()
    first_tissue.unsetWarpedTissue()
    self.tissue_container.append(first_tissue)

    second_tissue = Tissue()
    second_tissue.setTissueProbilityMapPath(tissue_proba_map_path)
    second_tissue.setTissueProbilityDimension(2)
    second_tissue.setGaussianNumber(2)
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

