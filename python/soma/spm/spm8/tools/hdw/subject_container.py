 # -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.tools.hdw.subject_container import SubjectContainer as SubjectContainer_virtual
from soma.spm.spm8.tools.hdw.subject import Subject
from soma.spm.spm_container import SPMContainer

class SubjectContainer(SubjectContainer_virtual, SPMContainer):
  def __init__(self):
    SPMContainer.__init__(self, Subject)
