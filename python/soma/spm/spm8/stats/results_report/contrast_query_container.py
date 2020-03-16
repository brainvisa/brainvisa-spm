# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.stats.results_report.contrast_query_container import ContrastQueryContainer as ContrastQueryContainer_virtual
from soma.spm.virtual_spm.stats.results_report.contrast_query import ContrastQuery

from soma.spm.spm_container import SPMContainer

class ContrastQueryContainer(ContrastQueryContainer_virtual, SPMContainer):
  def __init__(self):
    SPMContainer.__init__(self, ContrastQuery)
