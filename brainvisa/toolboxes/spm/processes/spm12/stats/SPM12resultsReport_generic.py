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
from soma.spm.spm12.stats.results_report import ResultsReport
from soma.spm.spm12.stats.results_report.contrast_query import ContrastQuery
from soma.spm.spm12.stats.results_report.masking import Contrast, Image
from soma.spm.spm12.stats.results_report.write_filtered_images import ThresholdedSPM, AllClustersBinary, AllClustersNAry

from soma.spm.spm_launcher import SPM12Standalone, SPM12

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
name = 'spm12 - Results report'

signature = Signature(
  'results_report_mat_file', ReadDiskItem('Matlab SPM file', 'Matlab file'),
  'data_type', Choice('Volumetric (2D/3D)',
                      'Scalp-Time',
                      'Scalp-Frequency',
                      'Time-Frequency',
                      'Frequency-Frequency'),
  'print_result', Choice("none",
                         "PostScript (PS)",
                         "Encapsulated PostScript (EPS)",
                         "Portable Document Format (PDF)",
                         "JPEG image",
                         "PNG image",
                         "TIFF image",
                         "MATLAB figure",
                         "CSV file",
                         "NIDM (Neuroimaging Data Model)"),
  'write_filtered_images', Choice(('Thresholded SPM', 'thresh'),
                                  ('All clusters (binary)', 'binary'),
                                  ('All clusters (n-ary)', 'n-ary')),
  'write_filtered_images_basename', String(),

  'add_section_overlay', Boolean(),
  'section_image', ReadDiskItem('anatomical Template', ['NIFTI-1 image', 'SPM image', 'MINC image']),
  'add_render_overlay', Boolean(),
  'render_image', ReadDiskItem('SPM Render', 'Matlab file'),
  'render_style', Choice(('New', '1'), ('Old', 'NaN')),
  'brightness', Choice(("Neither", 1), ('slightly', 0.75), ('more', 0.5), ('lots', 0.25)),
  'results_report', WriteDiskItem('Postscript file', 'PS file'),
  "results_report_directory", WriteDiskItem("Directory", "Directory"),
  "results_report_basename", String(),
  'contrast_number', Integer(),

  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script' ),
  'start_now', Boolean(),
)

def initialization( self ):

  self.setOptional("results_report_mat_file")  # because if spm pipeline in batch
  self.setOptional("results_report", "results_report_directory", "results_report_basename")
  self.addLink(None, 'add_section_overlay', self.updateSignatureAboutSection)
  self.addLink(None, 'add_render_overlay', self.updateSignatureAboutRender)
  self.addLink(None, 'render_style', self.updateSignatureAboutRender)
  self.addLink(None, "print_result", self._updateSignatureAboutOutputs)
  self.contrast_number = 0
  self.contrast_current_number = 0

  self.addLink(None, 'contrast_number', self.updateSignatureAboutSimpleContrastNumber)

  self.addLink("batch_location", "results_report_mat_file", self.updateBatchPath)

  self.write_filtered_images_basename = "filtered_images"
  self.add_section_overlay = False
  self.add_render_overlay = False

def updateSignatureAboutSection(self, proc):
  if self.add_section_overlay:
    self.setEnable('section_image')
  else:
    self.setDisable('section_image')
  self.changeSignature(self.signature)

def updateSignatureAboutRender(self, proc):
  if self.add_render_overlay:
    self.setEnable('render_image', 'render_style')
    if self.render_style == '1':
      self.setEnable('brightness')
    elif self.render_style == 'NaN':
      self.setDisable('brightness')
    else:
      raise ValueError('Unvalid render_style')
  else:
    self.setDisable('render_image', 'render_style', 'brightness')
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

def updateSignatureAboutSimpleContrastNumber(self, proc):
  if self.contrast_number < self.contrast_current_number:
    for contrast_index in range(self.contrast_number,self.contrast_current_number):
      self.removeSimpleContrastInSignature(contrast_index)
    self.changeSignature(self.signature)
  else:
    for contrast_index in range(self.contrast_current_number,self.contrast_number):
      self.addSimpleContrastInSignature(contrast_index)
      self.changeSignature(self.signature)
      self.initializeNewContrastFields(contrast_index)
  self.contrast_current_number = self.contrast_number

def removeSimpleContrastInSignature(self, contrast_index):
  del self.signature['contrast_' + str(contrast_index) + '_title']
  del self.signature['contrast_' + str(contrast_index) + '_index']
  del self.signature['contrast_' + str(contrast_index) + '_threshold_type']
  del self.signature['contrast_' + str(contrast_index) + '_threshold']
  del self.signature['contrast_' + str(contrast_index) + '_extent']
  del self.signature['contrast_' + str(contrast_index) + '_masking']
  del self.signature['contrast_' + str(contrast_index) + '_mask_index']
  del self.signature['contrast_' + str(contrast_index) + '_mask']
  del self.signature['contrast_' + str(contrast_index) + '_mask_threshold']
  del self.signature['contrast_' + str(contrast_index) + '_images_mask']


def addSimpleContrastInSignature(self, contrast_index):
  self.signature['contrast_' + str(contrast_index) + '_title'] = String()
  self.signature['contrast_' + str(contrast_index) + '_index'] = ListOf(Integer())
  self.signature['contrast_' + str(contrast_index) + '_threshold_type'] = Choice('FDR', 'FWE', "Neither")
  self.signature['contrast_' + str(contrast_index) + '_threshold'] = Float()
  self.signature['contrast_' + str(contrast_index) + '_extent'] = Integer()
  self.signature['contrast_' + str(contrast_index) + '_masking'] = Choice("None", "Contrast", "Image")
  self.signature['contrast_' + str(contrast_index) + '_mask_index'] = ListOf(Integer())
  self.signature['contrast_' + str(contrast_index) + '_mask_index'].mandatory = False
  self.signature['contrast_' + str(contrast_index) + '_mask'] = Choice('Inclusive', 'Exclusive')
  self.signature['contrast_' + str(contrast_index) + '_mask'].mandatory = False
  self.signature['contrast_' + str(contrast_index) + '_mask_threshold'] = Float()
  self.signature['contrast_' + str(contrast_index) + '_mask_threshold'].mandatory = False
  self.signature['contrast_' + str(contrast_index) + '_images_mask'] = ListOf(WriteDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image']))
  self.signature['contrast_' + str(contrast_index) + '_images_mask'].mandatory = False

def initializeNewContrastFields(self, contrast_index):
  self.setValue('contrast_' + str(contrast_index) + '_title', 'contrast_' + str(contrast_index))
  self.setValue('contrast_' + str(contrast_index) + '_index', contrast_index + 1)
  self.setValue('contrast_' + str(contrast_index) + '_threshold_type', "Neither")
  self.setValue('contrast_' + str(contrast_index) + '_threshold', 0.001)
  self.setValue('contrast_' + str(contrast_index) + '_extent', 0)
  self.setValue('contrast_' + str(contrast_index) + '_masking', "None")
  self.setValue('contrast_' + str(contrast_index) + '_mask_threshold', 0.05)

def updateBatchPath(self, proc):
  if self.results_report_mat_file is not None:
    directory_path = os.path.dirname(self.results_report_mat_file.fullPath())
    return os.path.join(directory_path, 'spm12_results_report_job.m')

def execution( self, context ):
  if self.add_section_overlay or self.add_render_overlay:
    if "-nodisplay" in configuration.matlab.options:
      r = context.ask('matlab.options contains -nodisplay, replace it by -nodesktop ?', 'yes', 'no')
      if r == 0:
        configuration.matlab.options = configuration.matlab.options.replace('-nodisplay', '-nodesktop')
      else:
        context.warning("nodisplay option is not working with render or section overlay, both will be disable")
        self.add_section_overlay = False
        self.add_render_overlay = False
    else:
      pass
  else:
    pass
  #spm_workspace_directory = os.path.dirname(self.batch_location.fullPath())

  result = self.createResultsReportBatch(context)
  spm = self.getSpmObject()
  for contrast_index in range(self.contrast_number):
    contrast_threshold_type = eval('self.contrast_' + str(contrast_index) + '_threshold_type')
    if contrast_threshold_type == "FDR":
      spm.addSPMCommandToExecutionQueue(["spm_get_defaults('stats.topoFDR', 0);"])
      continue
  spm.addModuleToExecutionQueue(result)
  if self.start_now:
    spm.setSPMScriptPath(self.batch_location.fullPath())
    if self.add_section_overlay:
      spm.addMatlabCommandAfterSPMRunning(self.addSectionScriptToSPMBatch())
    else:
      pass  # no section added
    if self.add_render_overlay:
      spm.addMatlabCommandAfterSPMRunning(self.addRenderScriptToSPMBatch())
    else:
      pass  # no render added

    output = spm.run()
    context.log(name, html=output)

def getSpmObject(self):
  if self.add_section_overlay or self.add_render_overlay:
    return SPM12(configuration.SPM.spm12_path,
                 configuration.matlab.executable,
                 configuration.matlab.options)
  else:
    return self.validation()

def createResultsReportBatch(self, context):

  result = ResultsReport()
  result.setMatlabFilePath(str(self.results_report_mat_file.fullPath()))
  if self.contrast_number != 0:
    for contrast_index in range(self.contrast_number):
      contrast = ContrastQuery()

      contrast_query_title = eval('self.contrast_' + str(contrast_index) + '_title')
      contrast.setTitle(contrast_query_title)

      contrast.setContrastIndexList([contrast_index + 1])#Matlab count start at 1, not 0

      contrast_threshold_type = eval('self.contrast_' + str(contrast_index) + '_threshold_type')
      if contrast_threshold_type == 'FWE':
        contrast.setThresholdToFWE()
      elif contrast_threshold_type == 'FDR':
        contrast.setThresholdToFDR()
      else:
        contrast.unsetThreshold()

      contrast_threshold = eval('self.contrast_' + str(contrast_index) + '_threshold')
      contrast.setThresholdValue(contrast_threshold)

      contrast_extent = eval('self.contrast_' + str(contrast_index) + '_extent')
      contrast.setExtentValue(contrast_extent)

      masking = eval('self.contrast_' + str(contrast_index) + '_masking')
      if masking == "None":
        contrast.unsetMasking()
      elif masking == "Contrast":
        masking_contrast = Contrast()

        mask_index_list = eval('self.contrast_' + str(contrast_index) + '_mask_index')
        masking_contrast.setContrastIndexList(mask_index_list)

        contrast_mask = eval('self.contrast_' + str(contrast_index) + '_mask')
        if contrast_mask == "Inclusive":
          masking_contrast.setNatureOfMaskToInclusive()
        elif contrast_mask == "Exclusive":
          masking_contrast.setNatureOfMaskToExclusive()

        contrast_mask_threshold = eval('self.contrast_' + str(contrast_index) + '_mask_threshold')
        if contrast_mask_threshold:
          masking_contrast.setMaskThreshold(contrast_mask_threshold)

        contrast.setMasking(masking_contrast)

      elif masking == "Image":
        masking_images = Image()

        contrast_mask = eval('self.contrast_' + str(contrast_index) + '_mask')
        if contrast_mask == "Inclusive":
          masking_images.setNatureOfMaskToInclusive()
        elif contrast_mask == "Exclusive":
          masking_images.setNatureOfMaskToExclusive()

        images = eval('self.contrast_' + str(contrast_index) + '_images_mask')
        masking_images.setMaskImagesPathList([diskitem.fullPath() for diskitem in images])
      else:
        raise ValueError("Unvalid masking choice")

      result.appendContrastQuery(contrast)

    if self.data_type == 'Volumetric (2D/3D)':
      result.setDataTypeToVolumetric()
    elif self.data_type == 'Scalp-Time':
      result.setDataTypeToScalpTime()
    elif self.data_type == 'Scalp-Frequency':
      result.setDataTypeToScalpFrequency()
    elif self.data_type == 'Time-Frequency':
      result.setDataTypeToTimeFrequency()
    elif self.data_type == 'Scalp-Frequency':
      result.setDataTypeToFrequencyFrequency()

    if self.print_result == "none":
      result.unsetPrintResults()
    elif self.print_result == "PostScript (PS)":
      result.setPrintResultsToPS()
    elif self.print_result == "Encapsulated PostScript (EPS)":
      result.setPrintResultsToEPS()
    elif self.print_result == "Portable Document Format (PDF)":
      result.setPrintResultsToPDF()
    elif self.print_result == "JPEG image":
      result.setPrintResultsToJPEG()
    elif self.print_result == "PNG image":
      result.setPrintResultsToPNG()
    elif self.print_result == "TIFF image":
      result.setPrintResultsToTIFF()
    elif self.print_result == "MATLAB figure":
      result.setPrintResultsToMatlabFigure()
    elif self.print_result == "CSV file":
      result.setPrintResultsToCSV()
    elif self.print_result == "NIDM (Neuroimaging Data Model)":
      result.setPrintResultsToNiDM()
    else:
      raise ValueError("Unvalid print_result choice")

    if self.print_result != "none":
      if self.print_result == "PostScript (PS)" and self.results_report is not None:
        result.setOutputResultPath(self.results_report.fullPath())
      elif self.results_report_directory is not None and self.results_report_basename:
        result.setOutputDirectoryAndBasename(self.results_report_directory.fullPath(), self.results_report_basename)
      else:
        pass#SPM default path used
    else:
      pass#result was not printed

    if self.write_filtered_images == "none":
      pass
    elif self.write_filtered_images == "thresh":
      threshold_spm = ThresholdedSPM()
      threshold_spm.setBasename(self.write_filtered_images_basename)
      result.setWriteFilteredImages(threshold_spm)
    elif self.write_filtered_images == "binary":
      all_cluster_binary = AllClustersBinary()
      all_cluster_binary.setBasename(self.write_filtered_images_basename)
      result.setWriteFilteredImages(all_cluster_binary)
    elif self.write_filtered_images == "n-ary":
      all_cluster_n_ary = AllClustersNAry()
      all_cluster_n_ary.setBasename(self.write_filtered_images_basename)
      result.setWriteFilteredImages(all_cluster_n_ary)


    return result
  else:
    raise ValueError("At least one contrast_number is mandatory")

#------------------------------------------------------------------------------
def addSectionScriptToSPMBatch(self):
  matlab_script_list = []
  matlab_script_list.append("spm_sections(xSPM,hReg,'%s');"% self.section_image.fullPath())
  matlab_script_list.append("choice = spm_input('Print section view',1,'Cancel|Print',[0,1],1)")
  matlab_script_list.append("""
if choice == 1
  spm_figure('Print');
end;""")
  return matlab_script_list


def addRenderScriptToSPMBatch(self):
  matlab_script_list = []
  matlab_script_list.extend(self.addRenderInitValueToSPMBatch())
  matlab_script_list.append("dat(1) = struct('XYZ', xSPM.XYZ,'t', xSPM.Z','mat', xSPM.M,'dim', xSPM.DIM);")
  matlab_script_list.append("spm_render(dat, %s, '%s');"% (self.render_style, self.render_image.fullPath()))
  matlab_script_list.append("spm_figure('Print');")
  return matlab_script_list

def addRenderInitValueToSPMBatch(self):
#  This script part is use to avoid the user intervention on SPM gui
# The color is set on RGB because the custom color choice is too hard to implement on Brainvisa. And usually users do not use it
  matlab_script_list = []
  matlab_script_list.append("global prevrend")
  matlab_script_list.append("prevrend = struct('rendfile','%s', 'brt',%g, 'col',eye(3));" % (self.render_image.fullPath(), self.brightness))
  return matlab_script_list

