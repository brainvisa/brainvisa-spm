# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm8.tools.dartel_tools.normalise_to_mni.subject import Subject
from soma.spm.virtual_spm.tools.dartel_tools.normalise_to_mni.few_subjects_container import FewSubjectsContainer as FewSubjectsContainer_virtual

from soma.spm.spm_container import SPMContainer


class FewSubjectsContainer(FewSubjectsContainer_virtual, SPMContainer):
  def __init__(self):
    SPMContainer.__init__(self, Subject)