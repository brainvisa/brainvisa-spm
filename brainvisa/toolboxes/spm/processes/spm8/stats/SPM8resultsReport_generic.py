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
from soma.spm.spm8.stats.results_report import ResultsReport
from soma.spm.spm8.stats.results_report.contrast_query import ContrastQuery
from soma.spm.spm8.stats.results_report.masking import Masking
from soma.spm.spm_launcher import SPM8

#------------------------------------------------------------------------------
configuration = Application().configuration
#------------------------------------------------------------------------------
def validation():
  spm = SPM8(configuration.SPM.spm8_path,
             configuration.matlab.executable,
             configuration.matlab.options)
  return spm
#------------------------------------------------------------------------------

userLevel = 0
name = 'spm8 - Results report'

signature = Signature(
  'results_report_mat_file', ReadDiskItem('Matlab SPM file', 'Matlab file'),
  'data_type', Choice('Volumetric (2D/3D)',
                      'Scalp-Time',
                      'Scalp-Frequency',
                      'Time-Frequency',
                      'Frequency-Frequency'),
  'print_result', Boolean(),

  'result_image_type', Choice(('Thresholded SPM', 'thresh'),
                              ('All clusters (binary)', 'binary'),
                              ('All clusters (n-ary)', 'n-ary')),
  'result_map', WriteDiskItem('4D Volume', 'SPM Image'),

  'add_section_overlay', Boolean(),
  'section_image', ReadDiskItem('anatomical Template', ['NIFTI-1 image', 'SPM image', 'MINC image']),
  'add_render_overlay', Boolean(),
  'render_image', ReadDiskItem('SPM Render', 'Matlab file'),
  'render_style', Choice(('New', '1'), ('Old', 'NaN')),
  'brightness', Choice(("Neither", 1), ('slightly', 0.75), ('more', 0.5), ('lots', 0.25)),
  'contrast_MIP', WriteDiskItem('Postscript file', 'PS file'),
  'copy_MIP_to_pdf', Boolean(),
  'contrast_MIP_pdf', WriteDiskItem('Postscript file', 'PDF file'),
  'contrast_number', Integer(),

  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script' ),


)

def initialization( self ):
  self.addLink(None, 'add_section_overlay', self.updateSignatureAboutSection)
  self.addLink(None, 'add_render_overlay', self.updateSignatureAboutRender)
  self.addLink(None, 'render_style', self.updateSignatureAboutRender)
  self.addLink(None, 'copy_MIP_to_pdf', self.updateSignatureAboutMIPPDF)
  self.contrast_number = 0
  self.contrast_current_number = 0

  self.addLink(None, 'contrast_number', self.updateSignatureAboutSimpleContrastNumber)

  self.addLink("batch_location", "results_report_mat_file", self.updateBatchPath)

  self.add_section_overlay = False
  self.add_render_overlay = False
  self.copy_MIP_to_pdf = False

  self.addLink('contrast_MIP_pdf', 'contrast_MIP')

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

def updateSignatureAboutMIPPDF(self, proc):
  if self.copy_MIP_to_pdf:
    self.setEnable('contrast_MIP_pdf')
  else:
    self.setDisable('contrast_MIP_pdf')
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


def addSimpleContrastInSignature(self, contrast_index):
  self.signature['contrast_' + str(contrast_index) + '_title'] = String()
  self.signature['contrast_' + str(contrast_index) + '_index'] = ListOf(Integer())
  self.signature['contrast_' + str(contrast_index) + '_threshold_type'] = Choice('FDR', 'FWE', "Neither")
  self.signature['contrast_' + str(contrast_index) + '_threshold'] = Float()
  self.signature['contrast_' + str(contrast_index) + '_extent'] = Integer()
  self.signature['contrast_' + str(contrast_index) + '_masking'] = Boolean()
  self.signature['contrast_' + str(contrast_index) + '_masking'].mandatory = False
  self.signature['contrast_' + str(contrast_index) + '_mask_index'] = ListOf(Integer())
  self.signature['contrast_' + str(contrast_index) + '_mask_index'].mandatory = False
  self.signature['contrast_' + str(contrast_index) + '_mask'] = Choice('Inclusive', 'Exclusive')
  self.signature['contrast_' + str(contrast_index) + '_mask'].mandatory = False
  self.signature['contrast_' + str(contrast_index) + '_mask_threshold'] = Float()
  self.signature['contrast_' + str(contrast_index) + '_mask_threshold'].mandatory = False

def initializeNewContrastFields(self, contrast_index):
  self.setValue('contrast_' + str(contrast_index) + '_title', 'contrast_' + str(contrast_index))
  self.setValue('contrast_' + str(contrast_index) + '_index', contrast_index + 1)
  self.setValue('contrast_' + str(contrast_index) + '_threshold_type', "Neither")
  self.setValue('contrast_' + str(contrast_index) + '_threshold', 0.001)
  self.setValue('contrast_' + str(contrast_index) + '_extent', 0)
  self.setValue('contrast_' + str(contrast_index) + '_masking', False)
  self.setValue('contrast_' + str(contrast_index) + '_mask_threshold', 0.05)

def updateBatchPath(self, proc):
  if self.results_report_mat_file is not None:
    directory_path = os.path.dirname(self.results_report_mat_file.fullPath())
    return os.path.join(directory_path, 'spm8_results_report_job.m')

def execution( self, context ):
  self.removeOldContrastMIPFile()

  spm_workspace_directory = os.path.dirname(self.batch_location.fullPath())

  result = self.createResultsReportBatch(context)
  spm = validation()#This is singleton object
  for contrast_index in range(self.contrast_number):
    contrast_threshold_type = eval('self.contrast_' + str(contrast_index) + '_threshold_type')
    if contrast_threshold_type == "FDR":
      spm.addSPMCommandToExecutionQueue(["spm_get_defaults('stats.topoFDR', 0);"])
      continue
  spm.addModuleToExecutionQueue(result)
  spm.setSPMScriptPath(self.batch_location.fullPath())
  spm.addMatlabCommandAfterSPMRunning(self.writeCompleteResultBatch(spm_workspace_directory))
  output = spm.run()
  context.log(name, html=output)

def removeOldContrastMIPFile(self):
  #By default SPM add to it so it is necessary to clean up before start
  if(os.path.exists(self.contrast_MIP.fullPath())):
    os.remove(self.contrast_MIP.fullPath())

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

      contrast_masking = eval('self.contrast_' + str(contrast_index) + '_masking')
      if contrast_masking:
        masking = Masking()

        mask_index_list = eval('self.contrast_' + str(contrast_index) + '_mask_index')
        masking.setContrastIndexList(mask_index_list)

        contrast_mask = eval('self.contrast_' + str(contrast_index) + '_mask')
        if contrast_mask == "Inclusive":
          masking.setNatureOfMaskToInclusive()
        elif contrast_mask == "Exclusive":
          masking.setNatureOfMaskToExclusive()

        contrast_mask_threshold = eval('self.contrast_' + str(contrast_index) + '_mask_threshold')
        if contrast_mask_threshold:
          masking.setMaskThreshold(contrast_mask_threshold)

        contrast.setMasking(masking)

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

    if self.print_result:
      result.enablePrintResult()
    else:
      result.disablePrintResult()

    return result
  else:
    raise ValueError("At least one contrast_number is mandatory")

#------------------------------------------------------------------------------
def writeCompleteResultBatch(self, spm_workspace_directory):
  stats_csv_path = os.path.join(spm_workspace_directory, "stats.csv")
  thresholding_info_path = os.path.join(spm_workspace_directory, "thresholding.info")

  matlab_script_list = []
  matlab_script_list.extend(self.addSpmWriteFilteredToSPMBatch())
  matlab_script_list.extend(addScriptAboutCSVStatToSPMBatch(stats_csv_path))
  matlab_script_list.extend(addScriptAboutThresholdingInfoToSPMBatch(thresholding_info_path))


  if self.add_section_overlay:
    matlab_script_list.extend(self.addSectionScriptToSPMBatch())
  if self.add_render_overlay:
    matlab_script_list.extend(self.addRenderScriptToSPMBatch())

  return matlab_script_list



def addSpmWriteFilteredToSPMBatch(self):
  matlab_script_list = []
  matlab_script_list.append("XYZ = xSPM.XYZ;")
  matlab_script_list.append("switch lower( '%s' )"% self.result_image_type)
  matlab_script_list.append("""
case 'thresh'
    Z = xSPM.Z;

case 'binary'
    Z = ones(size(xSPM.Z));

case 'n-ary'
    Z       = spm_clusters(XYZ);
    num     = max(Z);
    [n, ni] = sort(histc(Z,1:num), 2, 'descend');
    n       = size(ni);
    n(ni)   = 1:num;
    Z       = n(Z);
end""")
  matlab_script_list.append("spm_write_filtered( Z, XYZ, xSPM.DIM, xSPM.M, '', '%s' );" % self.result_map.fullPath())
  return matlab_script_list

def addScriptAboutCSVStatToSPMBatch(stats_csv_path):
  matlab_script_list = []
  matlab_script_list.append("tmpfile = [ '%s' ];" % stats_csv_path)
  matlab_script_list.append("fid = fopen(tmpfile,'wt');")
  matlab_script_list.append("fprintf(fid,[repmat('%s,',1,11) '%d,,\\n'],TabDat.hdr{1,:});")
  matlab_script_list.append("fprintf(fid,[repmat('%s,',1,12) '\\n'],TabDat.hdr{2,:});")
  matlab_script_list.append("fmt = TabDat.fmt;")
  matlab_script_list.append("[fmt{2,:}] = deal(','); fmt = [fmt{:}];")
  matlab_script_list.append("fmt(end:end+1) = '\\n'; fmt = strrep(fmt,' ',',');")
  matlab_script_list.append("""
for i=1:size(TabDat.dat,1)
  fprintf(fid,fmt,TabDat.dat{i,:});
end""")
  matlab_script_list.append("fclose(fid);")
  return matlab_script_list

def addScriptAboutThresholdingInfoToSPMBatch(thresholding_info_path):
  matlab_script_list = []
  matlab_script_list.append("tmpfile = [ '%s' ];" % thresholding_info_path)
  matlab_script_list.append("fid = fopen(tmpfile, 'wt');")
  matlab_script_list.append("fprintf(fid, '\\n' );")
  matlab_script_list.append("fprintf(fid, '%s', sprintf('Height threshold %c = %0.2f {%s}', xSPM.STAT, xSPM.u, xSPM.thresDesc));")
  matlab_script_list.append("fprintf(fid, '\\n' );")
  matlab_script_list.append("fprintf(fid, '%s', sprintf('Extent threshold k = %0.0f voxels', xSPM.k));")
  matlab_script_list.append("fclose(fid);")
  return matlab_script_list
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

#==============================================================================
#
#==============================================================================
def convertPSToPDF(context, ps_path, pdf_path):
  #if at least one path is too long ps2pdf doesn't work...
  tmp_ps = context.temporary('PS file')
  tmp_pdf = context.temporary('PDF file')
  shutil.copy(ps_path, tmp_ps.fullPath())

  command = ['ps2pdf', tmp_ps.fullPath(), tmp_pdf.fullPath()]
  context.system( *command )

  shutil.move(tmp_pdf.fullPath(), pdf_path)
