# -*- coding: utf-8 -*-
#  This software and supporting documentation are distributed by
#      Institut Federatif de Recherche 49
#      CEA/NeuroSpin, Batiment 145,
#      91191 Gif-sur-Yvette cedex
#      France
#
# This software is governed by the CeCILL license version 2 under
# French law and abiding by the rules of distribution of free software.
# You can  use, modify and/or redistribute the software under the
# terms of the CeCILL license version 2 as circulated by CEA, CNRS
# and INRIA at the following URL "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license version 2 and that you accept its terms.
from brainvisa.processes import *
from soma.spm.spm12.stats.model_review import ModelReview
from soma.spm.spm12.stats.model_review.display import DesignMatrix, DesignOrthogonality
from soma.spm.spm12.stats.model_review.display import FilesAndFactors, Covariates
from soma.spm.spm12.stats.model_review.display import Condition, CovarianceStructure

from soma.spm.spm_launcher import SPM12, SPM12Standalone
#------------------------------------------------------------------------------
configuration = Application().configuration
#------------------------------------------------------------------------------
def validation():
  try:
    spm = SPM12Standalone(configuration.SPM.spm12_standalone_command,
                          configuration.SPM.spm12_standalone_mcr_path,
                          configuration.SPM.spm12_standalone_path)
  except:
    spm = SPM12(configuration.SPM.spm12_path,
                configuration.matlab.executable,
                configuration.matlab.options)
  return spm
#------------------------------------------------------------------------------

userLevel = 0
name = 'spm12 - Model Review - generic'

signature = Signature(
  'basic_model_mat_file', ReadDiskItem('Matlab SPM file', 'Matlab file'),
  "display", Choice("Design Matrix",
                    "Design Orthogonality",
                    "Files & Factors",
                    "Covariates",
                    "Condition",
                    "Covariance Structure"),
  "session", ListOf(Integer()),
  "condition", ListOf(Integer()),
  'print_result', Choice("none",
                         "PostScript (PS)",
                         "Encapsulated PostScript (EPS)",
                         "Portable Document Format (PDF)",
                         "JPEG image",
                         "PNG image",
                         "TIFF image",
                         "MATLAB figure"),
  "results_report", WriteDiskItem("Any Type", "PS file"),
  "results_report_directory", WriteDiskItem("Directory", "Directory"),
  "results_report_basename", String(),
  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script' ),
  'start_now', Boolean(),
)

def initialization( self ):
  self.setOptional("basic_model_mat_file")  # because if spm pipeline in batch
  self.setOptional("results_report", "results_report_directory", "results_report_basename")

  self.display = "Design Matrix"
  self.print_result = "PostScript (PS)"

  self.addLink(None, "display", self.updateSignatureAboutDisplay)
  self.addLink(None, "print_result", self._updateSignatureAboutOutputs)

  self.addLink("batch_location", "basic_model_mat_file", self.updateBatchPath)

def updateSignatureAboutDisplay(self, display_choice, names, parameterized):
  if display_choice == "Condition":
    self.setEnable("session", "condition")
  else:
    self.setDisable("session", "condition")
  self.changeSignature(self.signature)

def _updateSignatureAboutOutputs(self, print_result, names, parameterized):
  if print_result == "none":
    self.setDisable("results_report", "results_report_directory", "results_report_basename")
  elif print_result == "PostScript (PS)":
    self.setEnable("results_report", mandatory=False)
    self.setDisable("results_report_directory", "results_report_basename")
  else:
    self.setEnable("results_report_directory", "results_report_basename", mandatory=False)
    self.setDisable("results_report")
  self.changeSignature(self.signature)

def updateBatchPath(self, proc):
  if self.basic_model_mat_file is not None:
    directory_path = os.path.dirname(self.basic_model_mat_file.fullPath())
    return os.path.join(directory_path, 'spm12_model_review_job.m')

def execution( self, context ):
  model_review = ModelReview()
  model_review.setMatlabFilePath(self.basic_model_mat_file.fullPath())

  if self.display == "Design Matrix":
    model_review.setDisplay(DesignMatrix())
  elif self.display == "Design Orthogonality":
    model_review.setDisplay(DesignOrthogonality())
  elif self.display == "Files & Factors":
    model_review.setDisplay(FilesAndFactors())
  elif self.display == "Covariates":
    model_review.setDisplay(Covariates())
  elif self.display == "Condition":
    display = Condition()
    display.setSessionIndexes(self.session)
    display.setConditionIndexes(self.condition)
    model_review.setDisplay(display)
  elif self.display == "Covariance Structure":
    model_review.setDisplay(CovarianceStructure())
  else:
    raise ValueError("Unvalid display choice")

  if self.print_result == "none":
    model_review.unsetPrintResults()
  elif self.print_result == "PostScript (PS)":
    model_review.setPrintResultsToPS()
  elif self.print_result == "Encapsulated PostScript (EPS)":
    model_review.setPrintResultsToEPS()
  elif self.print_result == "Portable Document Format (PDF)":
    model_review.setPrintResultsToPDF()
  elif self.print_result == "JPEG image":
    model_review.setPrintResultsToJPEG()
  elif self.print_result == "PNG image":
    model_review.setPrintResultsToPNG()
  elif self.print_result == "TIFF image":
    model_review.setPrintResultsToTIFF()
  elif self.print_result == "MATLAB figure":
    model_review.setPrintResultsToMatlabFigure()
  else:
    raise ValueError("Unvalid print_result choice")

  if self.print_result != "none":
    if self.print_result == "PostScript (PS)" and self.results_report is not None:
      model_review.setOutputResultPath(self.results_report.fullPath())
    elif self.results_report_directory is not None and self.results_report_basename:
      model_review.setOutputDirectoryAndBasename(self.results_report_directory.fullPath(), self.results_report_basename)
    else:
      pass#SPM default path used
  else:
    pass#result was not printed

  spm = validation()
  spm.addModuleToExecutionQueue(model_review)
  if self.start_now:
    spm.setSPMScriptPath(self.batch_location.fullPath())
    output = spm.run()
    context.log(name, html=output)


