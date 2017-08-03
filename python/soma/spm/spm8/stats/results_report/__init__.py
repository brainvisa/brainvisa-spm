# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.stats.results_report import ResultsReport as ResultsReport_virtual
from soma.spm.spm_main_module import SPM8MainModule

from soma.spm.spm8.stats.results_report.contrast_query_container import ContrastQueryContainer

class ResultsReport(ResultsReport_virtual, SPM8MainModule):
  def __init__(self):
    self.matlab_file_path = None
    self.contrast_query_container = ContrastQueryContainer()
    self.data_type = 1
    self.print_result = 'true'
