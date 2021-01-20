# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.tools.dartel_tools.normalise_to_mni.subject import Subject as Subject_virtual


class Subject(Subject_virtual):
  def __init__(self):
    self.flow_field_path_list = None
    self.image_path_list = None
    self.output_image_path_list = []

