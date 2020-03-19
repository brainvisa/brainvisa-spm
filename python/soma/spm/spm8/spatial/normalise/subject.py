# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.spatial.normalise.subject import SubjectToEstimate as SubjectToEstimate_virtual
from soma.spm.virtual_spm.spatial.normalise.subject import SubjectToEstimateAndWrite as SubjectToEstimateAndWrite_virtual
from soma.spm.virtual_spm.spatial.normalise.subject import SubjectToWrite as SubjectToWrite_virtual

import abc

import six


class Subject(six.with_metaclass(abc.ABCMeta)):
  pass

class SubjectToEstimate(SubjectToEstimate_virtual, Subject):
  def __init__(self):
    self.source_image_path = None
    self.source_weighting_image_path = ''
    self.sn_mat_filepath = None

class SubjectToEstimateAndWrite(SubjectToEstimateAndWrite_virtual, SubjectToEstimate):
  def __init__(self):
    SubjectToEstimate.__init__(self)
    self.image_path_list_to_write = None
    self.image_path_list_written = None

class SubjectToWrite(SubjectToWrite_virtual, Subject):
  def __init__(self):
    self.parameter_path = None
    self.image_path_list_to_write = None
    self.image_path_list_written = None
