# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.stats.results_report import ResultsReport as ResultsReport_virtual
from soma.spm.spm_main_module import SPM12MainModule
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.spm_batch_maker_utils import moveFileAndCreateFoldersIfNeeded
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
from soma.spm.spm_batch_maker_utils import getTodayDateInSpmFormat

from soma.spm.spm8.stats.results_report.contrast_query_container import ContrastQueryContainer
from soma.spm.spm12.stats.results_report.write_filtered_images import WriteFilteredImages

import os
import time

class ResultsReport(ResultsReport_virtual, SPM12MainModule):
  def __init__(self):
    self.matlab_file_path = None
    self.contrast_query_container = ContrastQueryContainer()
    self.data_type = 1
    self.print_result = "'ps'"

    self.output_results_path = None
    self.output_directory = None
    self.output_basename = None

  def enablePrintResult(self):
    raise NotImplementedError("it is deprecated in SPM12")

  def disablePrintResult(self):
    raise NotImplementedError("it is deprecated in SPM12")

  def unsetPrintResults(self):
    self.print_result = 'false'

  def setPrintResultsToPS(self):
    self.print_result = "'ps'"

  def setPrintResultsToEPS(self):
    self.print_result = "'eps'"

  def setPrintResultsToPDF(self):
    self.print_result = "'pdf'"

  def setPrintResultsToJPEG(self):
    self.print_result = "'jpg'"

  def setPrintResultsToPNG(self):
    self.print_result = "'png'"

  def setPrintResultsToTIFF(self):
    self.print_result = "'tif'"

  def setPrintResultsToMatlabFigure(self):
    self.print_result = "'fig'"

  def setPrintResultsToCSV(self):
    self.print_result = "'csv'"

  def setPrintResultsToNiDM(self):
    self.print_result = "'nidm'"

  def unsetWriteFilteredImages(self):
    self.write_filtered_images = None

  @checkIfArgumentTypeIsAllowed(WriteFilteredImages, 1)
  def setWriteFilteredImages(self, write_filtered_images):
    self.write_filtered_images = write_filtered_images

  def setOutputResultPath(self, output_results_path):
    self.output_results_path = output_results_path
    self.output_directory = None
    self.output_basename = None

  def setOutputDirectoryAndBasename(self, output_directory, output_basename):
    self.output_results_path = None
    self.output_directory = output_directory
    self.output_basename = output_basename

  def getStringListForBatch( self ):
    if self.matlab_file_path is not None:
      batch_list = []
      batch_list.append("spm.stats.results.spmmat = {'%s'};" % self.matlab_file_path)
      batch_list.append("spm.stats.results.units = %i;" % self.data_type)
      batch_list.append("spm.stats.results.print = %s;" % self.print_result)
      batch_list.extend(addBatchKeyWordInEachItem("spm.stats.results", self.contrast_query_container.getStringListForBatch()))
      if self.write_filtered_images is not None:
        batch_list.extend(addBatchKeyWordInEachItem("spm.stats.results", self.write_filtered_images.getStringListForBatch()))
      else:
        batch_list.append("spm.stats.results.write.none = 1;")
      return batch_list
    else:
      raise ValueError('Unvalid Model estimation, Mat file not found')

  def _moveSPMDefaultPathsIfNeeded(self):
    if self.print_result != 'false':
      spm_date = getTodayDateInSpmFormat()
      workspace_diretory = os.path.dirname(self.matlab_file_path)
      ext = self.print_result.replace("'", '')
      if self.print_result == "'nidm'":
        ext += ".zip"
      else:
        pass
      if self.output_results_path is not None:
        time.sleep(0.5)
        spm_result_path = os.path.join(workspace_diretory, "spm_%s.%s" % (spm_date, ext))
        if os.path.exists(spm_result_path):
          moveFileAndCreateFoldersIfNeeded(spm_result_path,
                                           self.output_results_path)
        else:
          raise RuntimeError("Output file not found")
      elif not None in [self.output_directory, self.output_basename]:
        time.sleep(0.5)
        if os.path.exists(os.path.join(workspace_diretory, "spm_%s_001.%s" % (spm_date, ext))):
          index = 1
          while(os.path.exists(os.path.join(workspace_diretory, "spm_%s_%03d.%s" % (spm_date, index, ext)))):
            output_results_path = os.path.join(self.output_directory, "%s_%03d.%s" % (self.output_basename, index, ext))
            moveFileAndCreateFoldersIfNeeded(os.path.join(workspace_diretory, "spm_%s_%03d.%s" % (spm_date, index, ext)),
                                             output_results_path)
            index += 1
        else:
          raise RuntimeError("Output file not found")
      else:
        time.sleep(0.5)
        pass#default prefix used
    else:
      pass#default prefix used
