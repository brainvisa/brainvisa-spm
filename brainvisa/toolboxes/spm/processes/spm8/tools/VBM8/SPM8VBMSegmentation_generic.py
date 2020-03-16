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
from __future__ import absolute_import
from brainvisa.processes import *
from soma.spm.spm8.tools.vbm import EstimateAndWrite
from soma.spm.spm8.tools.vbm.estimation_options import EstimationOptions
from soma.spm.spm8.tools.vbm.extended_options import ExtendedOptions
from soma.spm.spm8.tools.vbm.writing_options import WritingOptions, GreyMatterWritingOptions, WhiteMatterWritingOptions, CSFMatterWritingOptions, BiasCorrectedWritingOptions, PVELabelWritingOptions

from soma.spm.spm_launcher import SPM8, SPM8Standalone

#------------------------------------------------------------------------------
configuration = Application().configuration
#------------------------------------------------------------------------------
def validation():
  spm = SPM8(configuration.SPM.spm8_path,
             configuration.matlab.executable,
             configuration.matlab.options)
  return spm
#------------------------------------------------------------------------------

userLevel = 1
name = 'spm8 - VBM Segmentation - generic'

estimation_options_section = "Estimation options"
extended_options_section = "Extended options"
grey_matter_options_section = "Grey matter"
white_matter_options_section = "White matter"
csf_matter_options_section = "CSF matter"
bias_correction_options_section = "Bias correction"
PVE_options_section = "Partial Volume Effect"
jacobian_section = "Jacobian"
deformation_field = "Deformation fields"


signature = Signature(
  't1mri', ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image']),#Input volume

  #Estimation Options
  'TPM_template', ReadDiskItem('TPM template', ['NIFTI-1 image', 'SPM image', 'MINC image'], section=estimation_options_section),
  'gaussian_classes', ListOf(Integer(),section=estimation_options_section),
  'bias_regulatisation', Choice('no regularisation (0)',
                                'extremely light regularisation (0.00001)',
                                'very light regularisation (0.0001)',
                                'light regularisation (0.001)',
                                'medium regularisation (0.01)',
                                'heavy regularisation (0.1)',
                                'very heavy regularisation (1)',
                                'extremely heavy regularisation (10)',
                                section=estimation_options_section),
  'bias_FWHM', Choice('30mm cutoff',
                      '40mm cutoff',
                      '50mm cutoff',
                      '60mm cutoff',
                      '70mm cutoff',
                      '80mm cutoff',
                      '90mm cutoff',
                      '100mm cutoff',
                      '110mm cutoff',
                      '120mm cutoff',
                      '130mm cutoff',
                      '140mm cutoff',
                      '150mm cutoff',
                      'No correction',
                      section=estimation_options_section),
  'affine_regularisation', Choice("No Affine Registration",
                                  "ICBM space template - European brains",
                                  "ICBM space template - East Asian brains",
                                  "Average sized template",
                                  "No regularisation",
                                  section=estimation_options_section),
  'warping_regularisation',Integer(section=estimation_options_section),
  'sampling_distance', Float(section=estimation_options_section),

  #Extended Options
  'spatial_norm', Choice('Low-dimensional: SPM default', 'High-dimensional: Dartel', section=extended_options_section),
  'DARTEL_template', ReadDiskItem('TPM HDW DARTEL template', ["NIFTI-1 image", "SPM image", "MINC image"], section=extended_options_section),
  'sanlm', Choice('No denoising', 'Denoising', 'Denoising (multi-threaded)', section=extended_options_section),
  'mrf', Float(section=extended_options_section),
  'clean_up', Choice('Dont do cleanup', 'Light Clean', 'Thorough Clean', section=extended_options_section),
  'print_results', Boolean(section=extended_options_section),

  # Writing Options
    #Grey Matter
  'save_grey_native', Boolean(section=grey_matter_options_section),
  'grey_native', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=grey_matter_options_section),
  'save_grey_normalized', Boolean(section=grey_matter_options_section),
  'grey_LDW_warped_unmodulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=grey_matter_options_section),
  'grey_HDW_warped_unmodulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=grey_matter_options_section),
  'save_grey_modulated', Choice("Neither", 'affine + non-linear (SPM8 default)', 'non-linear only', section=grey_matter_options_section),
  'grey_LDW_warped_modulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=grey_matter_options_section),
  'grey_HDW_warped_modulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=grey_matter_options_section),
  'save_grey_dartel_imported', Choice("Neither", 'rigid (SPM8 default)', 'affine', section=grey_matter_options_section),
  'grey_dartel_imported', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=grey_matter_options_section),

    #White Matter
  'save_white_native', Boolean(section=white_matter_options_section),
  'white_native', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=white_matter_options_section),
  'save_white_normalized', Boolean(section=white_matter_options_section),
  'white_LDW_warped_unmodulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=white_matter_options_section),
  'white_HDW_warped_unmodulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=white_matter_options_section),
  'save_white_modulated', Choice("Neither", 'affine + non-linear (SPM8 default)', 'non-linear only', section=white_matter_options_section),
  'white_LDW_warped_modulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=white_matter_options_section),
  'white_HDW_warped_modulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=white_matter_options_section),
  'save_white_dartel_imported', Choice("Neither", 'rigid (SPM8 default)', 'affine', section=white_matter_options_section),
  'white_dartel_imported', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=white_matter_options_section),

    #CSF
  'save_csf_native', Boolean(section=csf_matter_options_section),
  'csf_native', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=csf_matter_options_section),
  'save_csf_normalized', Boolean(section=csf_matter_options_section),
  'csf_LDW_warped_unmodulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=csf_matter_options_section),
  'csf_HDW_warped_unmodulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=csf_matter_options_section),
  'save_csf_modulated', Choice("Neither", 'affine + non-linear (SPM8 default)', 'non-linear only', section=csf_matter_options_section),
  'csf_LDW_warped_modulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=csf_matter_options_section),
  'csf_HDW_warped_modulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=csf_matter_options_section),
  'save_csf_dartel_imported', Choice("Neither", 'rigid (SPM8 default)', 'affine', section=csf_matter_options_section),
  'csf_dartel_imported', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=csf_matter_options_section),

  #Bias Correction
  'save_bias_native', Boolean(section=bias_correction_options_section),
  't1mri_bias_corrected', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=bias_correction_options_section),
  'save_bias_normalized', Boolean(section=bias_correction_options_section),
  'bias_LDW_warped_unmodulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=bias_correction_options_section),
  'bias_HDW_warped_unmodulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=bias_correction_options_section),
  'save_bias_affine', Boolean(section=bias_correction_options_section),
  'bias_affine', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=bias_correction_options_section),

  #PVE label image
  'save_pve_native', Boolean(section=PVE_options_section),
  'pve_native', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=PVE_options_section),
  'save_pve_normalized', Boolean(section=PVE_options_section),
  'pve_LDW_warped_unmodulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=PVE_options_section),
  'pve_HDW_warped_unmodulated', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=PVE_options_section),
  'save_pve_dartel_imported', Choice("Neither", 'rigid (SPM8 default)', 'affine', section=PVE_options_section),
  'pve_dartel_imported', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=PVE_options_section),

  #Jacobian Determinant
  'save_jacobian_normalized', Boolean(section=jacobian_section),
  'jacobian_normalized', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=jacobian_section),

  #Deformation Fields
  'save_deformation_fields', Choice("Neither", 'Image->Template (forward)', 'Template->Image (inverse)', 'inverse + forward', section=deformation_field),
  'forward_LDW_field', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=deformation_field),
  'forward_HDW_field', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=deformation_field),
  'inverse_LDW_field', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=deformation_field),
  'inverse_HDW_field', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=deformation_field),
  'DF_transformation_matrix', WriteDiskItem('Matlab SPM file', 'Matlab file', section=deformation_field),

  #pfile.txt: GM, WM and CSF volume
  'GM_WM_CSF_volumes_txt', WriteDiskItem('Text file', 'Text file', section='default SPM outputs'),

  #Batch
  'batch_location', WriteDiskItem( 'Any Type', 'Matlab script', section='default SPM outputs' )
  )

def initialization(self):
  self.setOptional("DF_transformation_matrix", "GM_WM_CSF_volumes_txt")
  #Modify signature by links
  self.addLink(None, 'spatial_norm', self.updateSignatureAboutDartelTemplate)
  self.addLink(None, 'save_grey_native', self.updateSignatureAboutGreyNative)
  self.addLink(None, 'save_grey_normalized', self.updateSignatureAboutGreyNormalized)
  self.addLink(None, 'spatial_norm', self.updateSignatureAboutGreyNormalized)
  self.addLink(None, 'save_grey_modulated', self.updateSignatureAboutGreyModulated)
  self.addLink(None, 'spatial_norm', self.updateSignatureAboutGreyModulated)
  self.addLink(None, 'save_grey_dartel_imported', self.updateSignatureAboutGreyDartel)
  self.addLink(None, 'save_white_native', self.updateSignatureAboutWhiteNative)
  self.addLink(None, 'save_white_normalized', self.updateSignatureAboutWhiteNormalized)
  self.addLink(None, 'spatial_norm', self.updateSignatureAboutWhiteNormalized)
  self.addLink(None, 'save_white_modulated', self.updateSignatureAboutWhiteModulated)
  self.addLink(None, 'spatial_norm', self.updateSignatureAboutWhiteModulated)
  self.addLink(None, 'save_white_dartel_imported', self.updateSignatureAboutWhiteDartel)
  self.addLink(None, 'save_csf_native', self.updateSignatureAboutCSFNative)
  self.addLink(None, 'save_csf_normalized', self.updateSignatureAboutCSFNormalized)
  self.addLink(None, 'spatial_norm', self.updateSignatureAboutCSFNormalized)
  self.addLink(None, 'save_csf_modulated', self.updateSignatureAboutCSFModulated)
  self.addLink(None, 'spatial_norm', self.updateSignatureAboutCSFModulated)
  self.addLink(None, 'save_csf_dartel_imported', self.updateSignatureAboutCSFDartel)
  self.addLink(None, 'save_bias_native', self.updateSignatureAboutBiasNative)
  self.addLink(None, 'save_bias_normalized', self.updateSignatureAboutBiasNormalized)
  self.addLink(None, 'spatial_norm', self.updateSignatureAboutBiasNormalized)
  self.addLink(None, 'save_bias_affine', self.updateSignatureAboutBiasAffine)
  self.addLink(None, 'save_pve_native', self.updateSignatureAboutPVENative)
  self.addLink(None, 'save_pve_normalized', self.updateSignatureAboutPVENormalized)
  self.addLink(None, 'spatial_norm', self.updateSignatureAboutPVENormalized)
  self.addLink(None, 'save_pve_dartel_imported', self.updateSignatureAboutPVEDartel)
  self.addLink(None, 'save_jacobian_normalized', self.updateSignatureAboutJacobian)
  self.addLink(None, 'spatial_norm', self.updateSignatureAboutJacobian)
  self.addLink(None, 'save_deformation_fields', self.updateSignatureAboutDeformationField)
  self.addLink(None, 'spatial_norm', self.updateSignatureAboutDeformationField)

  self.addLink("batch_location", "grey_native", self.updateBatchPath)

  #SPM default initialisation
  self.gaussian_classes = [2, 2, 2, 3, 4, 2]
  self.bias_regulatisation = 'very light regularisation (0.0001)'
  self.bias_FWHM = '60mm cutoff'
  self.affine_regularisation = "ICBM space template - European brains"
  self.warping_regularisation = 4
  self.sampling_distance = 3
  self.spatial_norm = "High-dimensional: Dartel"
  self.sanlm = "Denoising (multi-threaded)"
  self.mrf = 0.15
  self.clean_up = "Light Clean"
  self.print_results = True

  self.save_grey_native = False
  self.save_grey_normalized = False
  self.save_grey_modulated = "non-linear only"
  self.save_grey_dartel_imported = "Neither"

  self.save_white_native = False
  self.save_white_normalized = False
  self.save_white_modulated = "non-linear only"
  self.save_white_dartel_imported = "Neither"

  self.save_csf_native = False
  self.save_csf_normalized = False
  self.save_csf_modulated = "Neither"
  self.save_csf_dartel_imported = "Neither"

  self.save_bias_native = False
  self.save_bias_normalized = True
  self.save_bias_affine = False

  self.save_pve_native = False
  self.save_pve_normalized = False
  self.save_pve_dartel_imported = "Neither"

  self.save_jacobian_normalized = False
  self.save_deformation_fields = "Neither"


def updateSignatureAboutDartelTemplate(self, proc):
  if self.spatial_norm == "High-dimensional: Dartel":
    self.setEnable("DARTEL_template", "save_jacobian_normalized")
    self.setDisable("grey_LDW_warped_unmodulated", "grey_LDW_warped_modulated",
                    "white_LDW_warped_unmodulated", "white_LDW_warped_modulated",
                    "csf_LDW_warped_unmodulated", "csf_LDW_warped_modulated",
                    "bias_LDW_warped_unmodulated",
                    "pve_LDW_warped_unmodulated",
                    "forward_LDW_field", "inverse_LDW_field")
  else:
    self.setDisable("DARTEL_template", "save_jacobian_normalized")
    self.setDisable("grey_HDW_warped_unmodulated", "grey_HDW_warped_modulated",
                    "white_HDW_warped_unmodulated", "white_HDW_warped_modulated",
                    "csf_HDW_warped_unmodulated", "csf_HDW_warped_modulated",
                    "bias_HDW_warped_unmodulated",
                    "pve_HDW_warped_unmodulated",
                    "forward_HDW_field", "inverse_HDW_field")
  self.changeSignature(self.signature)

#Grey links
def updateSignatureAboutGreyNative(self, proc):
  self.updateSignatureFieldToShow("save_grey_native", "grey_native")

def updateSignatureAboutGreyNormalized(self, proc):
  if self.spatial_norm == "High-dimensional: Dartel":
    self.updateSignatureFieldToShow("save_grey_normalized", "grey_HDW_warped_unmodulated")
  else:
    self.updateSignatureFieldToShow("save_grey_normalized", "grey_LDW_warped_unmodulated")

def updateSignatureAboutGreyModulated(self, proc):
  if self.spatial_norm == "High-dimensional: Dartel":
    self.updateSignatureFieldToShow("save_grey_modulated", "grey_HDW_warped_modulated")
  else:
    self.updateSignatureFieldToShow("save_grey_modulated", "grey_LDW_warped_modulated")

def updateSignatureAboutGreyDartel(self, proc):
  self.updateSignatureFieldToShow("save_grey_dartel_imported", "grey_dartel_imported")
#white links
def updateSignatureAboutWhiteNative(self, proc):
  self.updateSignatureFieldToShow("save_white_native", "white_native")

def updateSignatureAboutWhiteNormalized(self, proc):
  if self.spatial_norm == "High-dimensional: Dartel":
    self.updateSignatureFieldToShow("save_white_normalized", "white_HDW_warped_unmodulated")
  else:
    self.updateSignatureFieldToShow("save_white_normalized", "white_LDW_warped_unmodulated")

def updateSignatureAboutWhiteModulated(self, proc):
  if self.spatial_norm == "High-dimensional: Dartel":
    self.updateSignatureFieldToShow("save_white_modulated", "white_HDW_warped_modulated")
  else:
    self.updateSignatureFieldToShow("save_white_modulated", "white_LDW_warped_modulated")

def updateSignatureAboutWhiteDartel(self, proc):
  self.updateSignatureFieldToShow("save_white_dartel_imported", "white_dartel_imported")
#csf links
def updateSignatureAboutCSFNative(self, proc):
  self.updateSignatureFieldToShow("save_csf_native", "csf_native")

def updateSignatureAboutCSFNormalized(self, proc):
  if self.spatial_norm == "High-dimensional: Dartel":
    self.updateSignatureFieldToShow("save_csf_normalized", "csf_HDW_warped_unmodulated")
  else:
    self.updateSignatureFieldToShow("save_csf_normalized", "csf_LDW_warped_unmodulated")

def updateSignatureAboutCSFModulated(self, proc):
  if self.spatial_norm == "High-dimensional: Dartel":
    self.updateSignatureFieldToShow("save_csf_modulated", "csf_HDW_warped_modulated")
  else:
    self.updateSignatureFieldToShow("save_csf_modulated", "csf_LDW_warped_modulated")

def updateSignatureAboutCSFDartel(self, proc):
  self.updateSignatureFieldToShow("save_csf_dartel_imported", "csf_dartel_imported")
#Bias
def updateSignatureAboutBiasNative(self, proc):
  self.updateSignatureFieldToShow("save_bias_native", "t1mri_bias_corrected")

def updateSignatureAboutBiasNormalized(self, proc):
  if self.spatial_norm == "High-dimensional: Dartel":
    self.updateSignatureFieldToShow("save_bias_normalized", "bias_HDW_warped_unmodulated")
  else:
    self.updateSignatureFieldToShow("save_bias_normalized", "bias_LDW_warped_unmodulated")

def updateSignatureAboutBiasAffine(self, proc):
  self.updateSignatureFieldToShow("save_bias_affine", "bias_affine")
#PVE
def updateSignatureAboutPVENative(self, proc):
  self.updateSignatureFieldToShow("save_pve_native", "pve_native")

def updateSignatureAboutPVENormalized(self, proc):
  if self.spatial_norm == "High-dimensional: Dartel":
    self.updateSignatureFieldToShow("save_pve_normalized", "pve_HDW_warped_unmodulated")
  else:
    self.updateSignatureFieldToShow("save_pve_normalized", "pve_LDW_warped_unmodulated")

def updateSignatureAboutPVEDartel(self, proc):
  self.updateSignatureFieldToShow("save_pve_dartel_imported", "pve_dartel_imported")

#Jacobian
def updateSignatureAboutJacobian(self, proc):
  if self.spatial_norm == "High-dimensional: Dartel":
    self.updateSignatureFieldToShow("save_jacobian_normalized", "jacobian_normalized")
  else:
    self.setDisable("jacobian_normalized")
  self.signatureChangeNotifier.notify(self)

#Deformation field
def updateSignatureAboutDeformationField(self, proc):
  if self.save_deformation_fields in ["Image->Template (forward)", "inverse + forward"]:
    self.setEnable("forward_LDW_field")
    self.setEnable("forward_HDW_field")
  else:
    self.setDisable("forward_LDW_field")
    self.setDisable("forward_HDW_field")

  if self.save_deformation_fields in ["Template->Image (inverse)", "inverse + forward"]:
    self.setEnable("inverse_LDW_field")
    self.setEnable("inverse_HDW_field")
  else:
    self.setDisable("inverse_LDW_field")
    self.setDisable("inverse_HDW_field")
  self.updateSignatureAboutDartelTemplate(proc)

#-----------------------------------------------------------------------------------
def updateSignatureFieldToShow(self, field_to_check, field_to_modified):
  if eval("self." + field_to_check) in [False, "Neither"]:
    self.setDisable(field_to_modified)
  else:
    self.setEnable(field_to_modified)
  self.changeSignature(self.signature)
#-----------------------------------------------------------------------------------
def updateBatchPath(self, proc, dummy, norm):
  if self.spatial_norm == "Low-dimensional: SPM default":
    if self.grey_native is not None:
      directory_path = os.path.dirname(self.grey_native.fullPath())
      return os.path.join(directory_path, 'spm8_VBM_segmentation_job.m')
  elif self.spatial_norm == "High-dimensional: Dartel":
    if self.grey_HDW_warped_unmodulated is not None:
      directory_path = os.path.dirname(self.grey_HDW_warped_unmodulated.fullPath())
      return os.path.join(directory_path, 'spm8_VBM_segmentation_job.m')

def execution( self, context ):
  context.warning('The execution time is approximately 8 min')

  estimate_and_write = EstimateAndWrite()
  estimate_and_write.setVolumePath(str(self.t1mri.fullPath()))
  #=============================================================================
  #
  #=============================================================================
  est_option = EstimationOptions()
  est_option.setTissueProbilityMapPath(str(self.TPM_template.fullPath()))
  est_option.setGaussianPerClassesList(self.gaussian_classes)
  if self.bias_regulatisation == 'no regularisation (0)':
    est_option.unsetBiasRegularisation()
  elif self.bias_regulatisation == 'extremely light regularisation (0.00001)':
    est_option.setBiasRegularisationToExtremelyLight()
  elif self.bias_regulatisation == 'very light regularisation (0.0001)':
    est_option.setBiasRegularisationToVeryLight()
  elif self.bias_regulatisation == 'light regularisation (0.001)':
    est_option.setBiasRegularisationToLight()
  elif self.bias_regulatisation == 'medium regularisation (0.01)':
    est_option.setBiasRegularisationToMedium()
  elif self.bias_regulatisation == 'heavy regularisation (0.1)':
    est_option.setBiasRegularisationToHeavy()
  elif self.bias_regulatisation == 'very heavy regularisation (1)':
    est_option.setBiasRegularisationToVeryHeavy()
  elif self.bias_regulatisation == 'extremely heavy regularisation (10)':
    est_option.setBiasRegularisationToExtremelyHeavy()
  else:
    raise ValueError('Unvalid bias_regulatisation value')

  if self.bias_FWHM == '30mm cutoff':
    est_option.setBiasFWHMTo30cutoff()
  elif self.bias_FWHM == '40mm cutoff':
    est_option.setBiasFWHMTo40cutoff()
  elif self.bias_FWHM == '50mm cutoff':
    est_option.setBiasFWHMTo50cutoff()
  elif self.bias_FWHM == '60mm cutoff':
    est_option.setBiasFWHMTo60cutoff()
  elif self.bias_FWHM == '70mm cutoff':
    est_option.setBiasFWHMTo70cutoff()
  elif self.bias_FWHM == '80mm cutoff':
    est_option.setBiasFWHMTo80cutoff()
  elif self.bias_FWHM == '90mm cutoff':
    est_option.setBiasFWHMTo90cutoff()
  elif self.bias_FWHM == '100mm cutoff':
    est_option.setBiasFWHMTo100cutoff()
  elif self.bias_FWHM == '110mm cutoff':
    est_option.setBiasFWHMTo1100cutoff()
  elif self.bias_FWHM == '120mm cutoff':
    est_option.setBiasFWHMTo120cutoff()
  elif self.bias_FWHM == '130mm cutoff':
    est_option.setBiasFWHMTo130cutoff()
  elif self.bias_FWHM == '140mm cutoff':
    est_option.setBiasFWHMTo140cutoff()
  elif self.bias_FWHM == '150mm cutoff':
    est_option.setBiasFWHMTo150cutoff()
  elif self.bias_FWHM == 'No correction':
    est_option.unsetBiasFWHM()
  else:
    raise ValueError('Unvalid bias_FWHM value')

  if self.affine_regularisation == 'No Affine Registration':
    est_option.unsetAffineRegularisation()
  elif self.affine_regularisation == 'ICBM space template - European brains':
    est_option.setAffineRegularisationToEuropeanBrains()
  elif self.affine_regularisation == 'ICBM space template - East Asian brains':
    est_option.setAffineRegularisationToAsianBrains()
  elif self.affine_regularisation == 'Average sized template':
    est_option.setAffineRegularisationToAverageSizedTemplate()
  elif self.affine_regularisation == 'No regularisation':
    est_option.unsetRegularisation()
  else:
    raise ValueError('Unvalid affine_regularisation value')

  est_option.setWarpingRegularisation(self.warping_regularisation)
  est_option.setSamplingDistance(self.sampling_distance)

  #=============================================================================
  #
  #=============================================================================
  ext_options = ExtendedOptions()
  if self.spatial_norm == "High-dimensional: Dartel":
    dartel_normalization = True
    ext_options.setDartelSpatialNormalization()
    ext_options.setDartelTemplatePath(self.DARTEL_template.fullPath())
  elif self.spatial_norm == "Low-dimensional: SPM default":
    dartel_normalization = False
    ext_options.setSPMDefaultSpatialNormalization()
  else:
    raise ValueError('Unvalid spatial_norm value')

  if self.sanlm == "No denoising":
    ext_options.unsetSANLMDenoising()
  elif self.sanlm == "Denoising":
    ext_options.setSANLMDenoising()
  elif self.sanlm == "Denoising (multi-threaded)":
    ext_options.setSANLMDenoisingToMultiThreaded()
  else:
    raise ValueError('Unvalid sanlm value')

  ext_options.setMRFWeighting(self.mrf)

  if self.clean_up == "Dont do cleanup":
    ext_options.unsetCleanUp()
  elif self.clean_up == "Light Clean":
    ext_options.setCleanUpToLight()
  elif self.clean_up == "Thorough Clean":
    ext_options.setCleanUpToThorough()
  else:
    raise ValueError('Unvalid clean_up value')

  if self.print_results:
    ext_options.enableDisplayAndPrintResult()
  else:
    ext_options.disableDisplayAndPrintResult()

  #=============================================================================
  #
  #=============================================================================
  #Grey options
  grey_options = GreyMatterWritingOptions(dartel_normalization)
  if self.save_grey_native:
    grey_options.setNative()
    grey_options.setNativePath(self.grey_native.fullPath())
  else:
    grey_options.unsetNative()
  if self.save_grey_normalized:
    grey_options.setNormalized()
    if self.spatial_norm == "High-dimensional: Dartel":
      grey_options.setNormalizedPath(self.grey_HDW_warped_unmodulated.fullPath())
    else:
      grey_options.setNormalizedPath(self.grey_LDW_warped_unmodulated.fullPath())
  else:
    grey_options.unsetNormalized()
  if self.save_grey_modulated == "affine + non-linear (SPM8 default)":
    grey_options.setModulationToAffineAndNonLinear()
    if self.spatial_norm == "High-dimensional: Dartel":
      grey_options.setModulatedAffineAndNonLinearPath(self.grey_HDW_warped_modulated.fullPath())
    else:
      grey_options.setModulatedAffineAndNonLinearPath(self.grey_LDW_warped_modulated.fullPath())
  elif self.save_grey_modulated == "non-linear only":
    grey_options.setModulationToNonLinear()
    if self.spatial_norm == "High-dimensional: Dartel":
      grey_options.setModulatedNonLinearPath(self.grey_HDW_warped_modulated.fullPath())
    else:
      grey_options.setModulatedNonLinearPath(self.grey_LDW_warped_modulated.fullPath())
  else:
    grey_options.unsetModulation()
  if self.save_grey_dartel_imported == "rigid (SPM8 default)":
    grey_options.setDartelExportToRigid()
    grey_options.setDartelRigidPath(self.grey_dartel_imported.fullPath())
  elif self.save_grey_dartel_imported == "affine":
    grey_options.setDartelExportToAffine()
    grey_options.setDartelAffinePath(self.grey_dartel_imported.fullPath())
  else:
    grey_options.unsetDartelExport()
  #=============================================================================
  #white options
  white_options = WhiteMatterWritingOptions(dartel_normalization)
  if self.save_white_native:
    white_options.setNative()
    white_options.setNativePath(self.white_native.fullPath())
  else:
    white_options.unsetNative()
  if self.save_white_normalized:
    white_options.setNormalized()
    if self.spatial_norm == "High-dimensional: Dartel":
      white_options.setNormalizedPath(self.white_HDW_warped_unmodulated.fullPath())
    else:
      white_options.setNormalizedPath(self.white_LDW_warped_unmodulated.fullPath())
  else:
    white_options.unsetNormalized()
  if self.save_white_modulated == "affine + non-linear (SPM8 default)":
    white_options.setModulationToAffineAndNonLinear()
    if self.spatial_norm == "High-dimensional: Dartel":
      white_options.setModulatedAffineAndNonLinearPath(self.white_HDW_warped_modulated.fullPath())
    else:
      white_options.setModulatedAffineAndNonLinearPath(self.white_LDW_warped_modulated.fullPath())
  elif self.save_white_modulated == "non-linear only":
    white_options.setModulationToNonLinear()
    if self.spatial_norm == "High-dimensional: Dartel":
      white_options.setModulatedNonLinearPath(self.white_HDW_warped_modulated.fullPath())
    else:
      white_options.setModulatedNonLinearPath(self.white_LDW_warped_modulated.fullPath())
  else:
    white_options.unsetModulation()
  if self.save_white_dartel_imported == "rigid (SPM8 default)":
    white_options.setDartelExportToRigid()
    white_options.setDartelRigidPath(self.white_dartel_imported.fullPath())
  elif self.save_white_dartel_imported == "affine":
    white_options.setDartelExportToAffine()
    white_options.setDartelAffinePath(self.white_dartel_imported.fullPath())
  else:
    white_options.unsetDartelExport()
  #=============================================================================
  #CSF options
  csf_options = CSFMatterWritingOptions(dartel_normalization)
  if self.save_csf_native:
    csf_options.setNative()
    csf_options.setNativePath(self.csf_native.fullPath())
  else:
    csf_options.unsetNative()
  if self.save_csf_normalized:
    csf_options.setNormalized()
    if self.spatial_norm == "High-dimensional: Dartel":
      csf_options.setNormalizedPath(self.csf_HDW_warped_unmodulated.fullPath())
    else:
      csf_options.setNormalizedPath(self.csf_LDW_warped_unmodulated.fullPath())
  else:
    csf_options.unsetNormalized()
  if self.save_csf_modulated == "affine + non-linear (SPM8 default)":
    csf_options.setModulationToAffineAndNonLinear()
    if self.spatial_norm == "High-dimensional: Dartel":
      csf_options.setModulatedAffineAndNonLinearPath(self.csf_HDW_warped_modulated.fullPath())
    else:
      csf_options.setModulatedAffineAndNonLinearPath(self.csf_LDW_warped_modulated.fullPath())
  elif self.save_csf_modulated == "non-linear only":
    csf_options.setModulationToNonLinear()
    if self.spatial_norm == "High-dimensional: Dartel":
      csf_options.setModulatedNonLinearPath(self.csf_HDW_warped_modulated.fullPath())
    else:
      csf_options.setModulatedNonLinearPath(self.csf_LDW_warped_modulated.fullPath())
  else:
    csf_options.unsetModulation()
  if self.save_csf_dartel_imported == "rigid (SPM8 default)":
    csf_options.setDartelExportToRigid()
    csf_options.setDartelRigidPath(self.csf_dartel_imported.fullPath())
  elif self.save_csf_dartel_imported == "affine":
    csf_options.setDartelExportToAffine()
    csf_options.setDartelAffinePath(self.csf_dartel_imported.fullPath())
  else:
    csf_options.unsetDartelExport()
  #=============================================================================
  #Bias options
  bias_options = BiasCorrectedWritingOptions(dartel_normalization)
  if self.save_bias_native:
    bias_options.setNative()
    bias_options.setNativePath(self.t1mri_bias_corrected.fullPath())
  else:
    bias_options.unsetNative()
  if self.save_bias_normalized:
    bias_options.setNormalized()
    if self.spatial_norm == "High-dimensional: Dartel":
      bias_options.setNormalizedPath(self.bias_HDW_warped_unmodulated.fullPath())
    else:
      bias_options.setNormalizedPath(self.bias_LDW_warped_unmodulated.fullPath())
  else:
    bias_options.unsetNormalized()
  if self.save_bias_affine:
    bias_options.setAffine()
    bias_options.setAffinePath(self.bias_affine.fullPath())
  else:
    bias_options.unsetAffine()
  #=============================================================================
  #PVE options
  pve_options = PVELabelWritingOptions(dartel_normalization)
  if self.save_pve_native:
    pve_options.setNative()
    pve_options.setNativePath(self.pve_native.fullPath())
  else:
    pve_options.unsetNative()
  if self.save_pve_normalized:
    pve_options.setNormalized()
    if self.spatial_norm == "High-dimensional: Dartel":
      pve_options.setNormalizedPath(self.pve_HDW_warped_unmodulated.fullPath())
    else:
      pve_options.setNormalizedPath(self.pve_LDW_warped_unmodulated.fullPath())
  else:
    pve_options.unsetNormalized()
  if self.save_pve_dartel_imported == "rigid (SPM8 default)":
    pve_options.setDartelExportToRigid()
    pve_options.setDartelRigidPath(self.pve_dartel_imported.fullPath())
  elif self.save_pve_dartel_imported == "affine":
    pve_options.setDartelExportToAffine()
    pve_options.setDartelAffinePath(self.pve_dartel_imported.fullPath())
  else:
    pve_options.unsetDartelExport()
#===============================================================================
#
#===============================================================================
  wri_options = WritingOptions(dartel_normalization)
  #Standard SPM output
  #=============================================================================
  if self.save_jacobian_normalized:
    wri_options.saveJacobianNormalized()
    wri_options.setJacobianPath(self.jacobian_normalized.fullPath())
  else:
    wri_options.discardJacobianNormalized()
  if self.save_deformation_fields in ["Image->Template (forward)"]:
    wri_options.saveDeformationFieldForward()
    if self.spatial_norm == "Low-dimensional: SPM default":
      wri_options.setDeformationFieldPath(self.forward_LDW_field.fullPath())
    elif self.spatial_norm == "High-dimensional: Dartel":
      wri_options.setDeformationFieldPath(self.forward_HDW_field.fullPath())
    else:
      raise ValueError("Unvalid spatial_norm")
  elif self.save_deformation_fields in ["Template->Image (inverse)"]:
    wri_options.saveDeformationFieldInverse()
    if self.spatial_norm == "Low-dimensional: SPM default":
      wri_options.setInverseDeformationFieldPath(self.inverse_LDW_field.fullPath())
    elif self.spatial_norm == "High-dimensional: Dartel":
      wri_options.setInverseDeformationFieldPath(self.inverse_HDW_field.fullPath())
    else:
      raise ValueError("Unvalid spatial_norm")
  elif self.save_deformation_fields in ["inverse + forward"]:
    wri_options.saveDeformationFieldInverseAndForward()
    if self.spatial_norm == "Low-dimensional: SPM default":
      wri_options.setDeformationFieldPath(self.forward_LDW_field.fullPath())
      wri_options.setInverseDeformationFieldPath(self.inverse_LDW_field.fullPath())
    elif self.spatial_norm == "High-dimensional: Dartel":
      wri_options.setDeformationFieldPath(self.forward_HDW_field.fullPath())
      wri_options.setInverseDeformationFieldPath(self.inverse_HDW_field.fullPath())
    else:
      raise ValueError("Unvalid spatial_norm")
  else:#"Neither"
    wri_options.discardDeformationField()

  if self.DF_transformation_matrix is not None:
    wri_options.setDeformationMatrixPath(self.DF_transformation_matrix.fullPath())
  if self.GM_WM_CSF_volumes_txt is not None:
    wri_options.setMatterVolumesPath(self.GM_WM_CSF_volumes_txt.fullPath())
  wri_options.replaceGreyMatterWritingOptions(grey_options)
  wri_options.replaceWhiteMatterWritingOptions(white_options)
  wri_options.replaceCSFMatterWritingOptions(csf_options)
  wri_options.replaceBiasCorrectedWritingOptions(bias_options)
  wri_options.replacePVELabelWritingOptions(pve_options)

  estimate_and_write.replaceEstimationOptions(est_option)
  estimate_and_write.replaceExtendedOptions(ext_options)
  estimate_and_write.replaceWritingOptions(wri_options)

  spm = validation()
  spm.addModuleToExecutionQueue(estimate_and_write)
  spm.setSPMScriptPath(self.batch_location.fullPath())
  output = spm.run()
  context.log(name, html=output)
