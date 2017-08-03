# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.tools.dartel_tools.normalise_to_mni.many_subjects import ManySubjects as ManySubjects_virtual

class ManySubjects(ManySubjects_virtual):
  def __init__(self):
    self.flow_field_path_list = None
    self.image_path_list_list = []
    self.output_image_path_list_list = []
