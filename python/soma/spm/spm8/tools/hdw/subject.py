 # -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.tools.hdw.subject import Subject as Subject_virtual

class Subject(Subject_virtual):
  def __init__(self):
    self.reference_image_path = None
    self.moved_image_path = None
    
    self.output_deformation_field_path = None
    self.output_jacobian_determinant_path = None