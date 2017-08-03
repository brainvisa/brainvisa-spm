# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.spatial.new_segment.channel_container import ChannelContainer as ChannelContainer_virtual
from soma.spm.spm8.spatial.new_segment.channel import Channel
from soma.spm.spm_container import SPMContainer

class ChannelContainer(ChannelContainer_virtual, SPMContainer):
  def __init__(self):
    SPMContainer.__init__(self, Channel)

