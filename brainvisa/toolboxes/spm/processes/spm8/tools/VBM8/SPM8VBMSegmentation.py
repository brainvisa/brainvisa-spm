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
from soma.spm.spm_launcher import SPM8, SPM8Standalone

#------------------------------------------------------------------------------
configuration = Application().configuration
#------------------------------------------------------------------------------
def validation():
  try:
    spm = SPM8Standalone(configuration.SPM.spm8_standalone_command,
                         configuration.SPM.spm8_standalone_mcr_path,
                         configuration.SPM.spm8_standalone_path)
  except:
    spm = SPM8(configuration.SPM.spm8_path,
               configuration.matlab.executable,
               configuration.matlab.options)
  return spm
#------------------------------------------------------------------------------

userLevel = 0
name = 'spm8 - VBM Segmentation'

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
  't1mri', ReadDiskItem('Raw T1 MRI', ['NIFTI-1 image', 'SPM image', 'MINC image']),#Input volume
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
  'DARTEL_template', ReadDiskItem('TPM HDW DARTEL template', ['NIFTI-1 image', 'SPM image', 'MINC image'], section=extended_options_section),
  'sanlm', Choice('No denoising', 'Denoising', 'Denoising (multi-threaded)', section=extended_options_section),
  'mrf', Float(section=extended_options_section),
  'clean_up', Choice('Dont do cleanup', 'Light Clean', 'Thorough Clean', section=extended_options_section),
  'print_results', Boolean(section=extended_options_section),

  # Writing Options
    #Grey Matter
  'save_grey_native', Boolean(section=grey_matter_options_section),
  'grey_native',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes={'tissue_class':'grey',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=grey_matter_options_section),
  'save_grey_normalized', Boolean(section=grey_matter_options_section),
  #'grey_normalized',
  'grey_LDW_warped_unmodulated',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes={'tissue_class':'grey',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'low-dimensional'},
                section=grey_matter_options_section),
  #'grey_DARTEL_normalized'
  'grey_HDW_warped_unmodulated',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes={'tissue_class':'grey',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'high-dimensional'},
                section=grey_matter_options_section),
  'save_grey_modulated', Choice("Neither", 'affine + non-linear (SPM8 default)', 'non-linear only', section=grey_matter_options_section),
  #'grey_modulated',
  'grey_LDW_warped_modulated',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes = {'tissue_class':'grey',
                                      'transformation':'none',
                                      'modulation':'affine and non-linear',
                                      'warping_method':'low-dimensional'},
                section=grey_matter_options_section),
  #'grey_DARTEL_modulated'
  'grey_HDW_warped_modulated',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes = {'tissue_class':'grey',
                                      'transformation':'none',
                                      'modulation':'affine and non-linear',
                                      'warping_method':'high-dimensional'},
                section=grey_matter_options_section),
  'save_grey_dartel_imported', Choice("Neither", 'rigid (SPM8 default)', 'affine', section=grey_matter_options_section),

  'grey_dartel_imported',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes={'tissue_class':'grey',
                                    'transformation':'rigid',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=grey_matter_options_section),

    #White Matter
  'save_white_native', Boolean(section=white_matter_options_section),
  'white_native',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes={'tissue_class':'white',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=white_matter_options_section),
  'save_white_normalized', Boolean(section=white_matter_options_section),
  #'white_normalized',
  'white_LDW_warped_unmodulated',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes={'tissue_class':'white',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'low-dimensional'},
                section=white_matter_options_section),
  #'white_DARTEL_normalized'
  'white_HDW_warped_unmodulated',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes={'tissue_class':'white',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'high-dimensional'},
                section=white_matter_options_section),
  'save_white_modulated', Choice("Neither", 'affine + non-linear (SPM8 default)', 'non-linear only', section=white_matter_options_section),
  #'white_modulated',
  'white_LDW_warped_modulated',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes = {'tissue_class':'white',
                                      'transformation':'none',
                                      'modulation':'affine and non-linear',
                                      'warping_method':'low-dimensional'},
                section=white_matter_options_section),
  #'white_DARTEL_modulated'
  'white_HDW_warped_modulated',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes = {'tissue_class':'white',
                                      'transformation':'none',
                                      'modulation':'affine and non-linear',
                                      'warping_method':'high-dimensional'},
                section=white_matter_options_section),
  'save_white_dartel_imported', Choice("Neither", 'rigid (SPM8 default)', 'affine', section=white_matter_options_section),

  'white_dartel_imported',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes={'tissue_class':'white',
                                    'transformation':'rigid',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=white_matter_options_section),
    #CSF
  'save_csf_native', Boolean(section=csf_matter_options_section),
  'csf_native',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes={'tissue_class':'csf',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=csf_matter_options_section),
  'save_csf_normalized', Boolean(section=csf_matter_options_section),
  #'csf_normalized',
  'csf_LDW_warped_unmodulated',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes={'tissue_class':'csf',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'low-dimensional'},
                section=csf_matter_options_section),
  #'csf_DARTEL_normalized'
  'csf_HDW_warped_unmodulated',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes={'tissue_class':'csf',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'high-dimensional'},
                section=csf_matter_options_section),
  'save_csf_modulated', Choice("Neither", 'affine + non-linear (SPM8 default)', 'non-linear only', section=csf_matter_options_section),
  #'csf_modulated',
  'csf_LDW_warped_modulated',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes = {'tissue_class':'csf',
                                      'transformation':'none',
                                      'modulation':'affine and non-linear',
                                      'warping_method':'low-dimensional'},
                section=csf_matter_options_section),
  #'csf_DARTEL_modulated'
  'csf_HDW_warped_modulated',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes = {'tissue_class':'csf',
                                      'transformation':'none',
                                      'modulation':'affine and non-linear',
                                      'warping_method':'high-dimensional'},
                section=csf_matter_options_section),
  'save_csf_dartel_imported', Choice("Neither", 'rigid (SPM8 default)', 'affine', section=csf_matter_options_section),

  'csf_dartel_imported',
  WriteDiskItem('T1 MRI tissue probability map',
                'NIFTI-1 image',
                requiredAttributes={'tissue_class':'csf',
                                    'transformation':'rigid',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=csf_matter_options_section),
  #Bias Correction
  'save_bias_native', Boolean(section=bias_correction_options_section),
  't1mri_bias_corrected',
  WriteDiskItem('T1 MRI Bias Corrected', 'NIFTI-1 image',
                requiredAttributes={'transformation':'none',
                                    'warping_method':'none',
                                    'space':'t1mri'},
                section=bias_correction_options_section),
  'save_bias_normalized', Boolean(section=bias_correction_options_section),
  'bias_LDW_warped_unmodulated',
  WriteDiskItem('T1 MRI Bias Corrected', 'NIFTI-1 image',
                requiredAttributes={'transformation':'none',
                                    'warping_method':'low-dimensional',
                                    'space':'mni'},
                section=bias_correction_options_section),
  'bias_HDW_warped_unmodulated',
  WriteDiskItem('T1 MRI Bias Corrected', 'NIFTI-1 image',
                requiredAttributes={'transformation':'none',
                                    'warping_method':'high-dimensional'},
                section=bias_correction_options_section),
  'save_bias_affine', Boolean(section=bias_correction_options_section),
  'bias_affine',
  WriteDiskItem('T1 MRI Bias Corrected', 'NIFTI-1 image',
                requiredAttributes={'transformation':'affine',
                                    'warping_method':'none',
                                    'space':'mni'},
               section=bias_correction_options_section),

  #PVE label image
  'save_pve_native', Boolean(section=PVE_options_section),
  'pve_native',
  WriteDiskItem('T1 MRI partial volume estimation',
                'NIFTI-1 image',
                requiredAttributes={'transformation':'none',
                                    'warping_method':'none'},
                section=PVE_options_section),
  'save_pve_normalized', Boolean(section=PVE_options_section),
  'pve_LDW_warped_unmodulated',
  WriteDiskItem('T1 MRI partial volume estimation',
                'NIFTI-1 image',
                requiredAttributes={'transformation':'none',
                                    'warping_method':'low-dimensional'},
                section=PVE_options_section),
  'pve_HDW_warped_unmodulated',
  WriteDiskItem('T1 MRI partial volume estimation',
                'NIFTI-1 image',
                requiredAttributes={'transformation':'none',
                                    'warping_method':'high-dimensional'},
                section=PVE_options_section),
  'save_pve_dartel_imported', Choice("Neither", 'rigid (SPM8 default)', 'affine', section=PVE_options_section),
  'pve_dartel_imported',
  WriteDiskItem('T1 MRI partial volume estimation',
                'NIFTI-1 image',
                requiredAttributes={'transformation':'rigid',
                                    'warping_method':'none'},
                section=PVE_options_section),

  #Jacobian Determinant
  'save_jacobian_normalized', Boolean(section=jacobian_section),
  'jacobian_normalized', WriteDiskItem('Jacobian determinant', 'NIFTI-1 image', section=jacobian_section),

  #Deformation Fields
  'save_deformation_fields', Choice("Neither", 'Image->Template (forward)', 'Template->Image (inverse)', 'inverse + forward', section=deformation_field),
  'forward_LDW_field',
  WriteDiskItem('SPM deformation field',
                'NIFTI-1 image',
                requiredAttributes = {'direction':'forward',
                                      'warping_method':'low-dimensional'},
                section=deformation_field),
  'forward_HDW_field',
  WriteDiskItem('SPM deformation field',
                'NIFTI-1 image',
                requiredAttributes = {'direction':'forward',
                                      'warping_method':'high-dimensional'},
                section=deformation_field),
  'inverse_LDW_field',
  WriteDiskItem('SPM deformation field',
                'NIFTI-1 image',
                requiredAttributes = {'direction':'inverse',
                                      'warping_method':'low-dimensional'},
                section=deformation_field),
  'inverse_HDW_field',
  WriteDiskItem('SPM deformation field',
                'NIFTI-1 image',
                requiredAttributes = {'direction':'inverse',
                                      'warping_method':'high-dimensional'},
                section=deformation_field),
  'DF_transformation_matrix', WriteDiskItem('Matlab SPM file', 'Matlab file', section=deformation_field),

  #pfile.txt: GM, WM and CSF volume
  'GM_WM_CSF_volumes_txt', WriteDiskItem('Estimate T1 MRI raw volumes', 'Text file', section='default SPM outputs'),

  #Batch
  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script', section='default SPM outputs' )
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

  self.addLink("batch_location", ("grey_native", "grey_HDW_warped_unmodulated", "spatial_norm"), self.updateBatchPath)
  self.addLink("DF_transformation_matrix", ("grey_native", "grey_HDW_warped_unmodulated", "spatial_norm"), self.updateTransformMatrix)

  self.linkParameters("grey_native", ("t1mri", "TPM_template"), self.updateGreyNative )
  self.linkParameters("grey_LDW_warped_unmodulated", "grey_native")
  self.linkParameters("grey_HDW_warped_unmodulated", ("grey_native", "DARTEL_template"), self.updateHDWGrey)
  self.linkParameters("grey_LDW_warped_modulated", "grey_native")
  self.linkParameters("grey_HDW_warped_modulated", "grey_HDW_warped_unmodulated")
  self.linkParameters("grey_dartel_imported", "grey_native")

  self.linkParameters("white_native", "grey_native" )
  self.linkParameters("white_LDW_warped_unmodulated", "grey_native")
  self.linkParameters("white_HDW_warped_unmodulated", "grey_HDW_warped_unmodulated")
  self.linkParameters("white_LDW_warped_modulated", "grey_native")
  self.linkParameters("white_HDW_warped_modulated", "grey_HDW_warped_unmodulated")
  self.linkParameters("white_dartel_imported", "grey_native")

  self.linkParameters("csf_native", "grey_native" )
  self.linkParameters("csf_LDW_warped_unmodulated", "grey_native")
  self.linkParameters("csf_HDW_warped_unmodulated", "grey_HDW_warped_unmodulated")
  self.linkParameters("csf_LDW_warped_modulated", "grey_native")
  self.linkParameters("csf_HDW_warped_modulated", "grey_HDW_warped_unmodulated")
  self.linkParameters("csf_dartel_imported", "grey_native")

  self.linkParameters("t1mri_bias_corrected", "grey_native", self.updateT1MRIBiasCorrected )
  self.linkParameters("bias_LDW_warped_unmodulated", "t1mri_bias_corrected")
  self.linkParameters("bias_HDW_warped_unmodulated", "grey_HDW_warped_unmodulated", self.updateT1MRIBiasCorrectedHDW)
  self.linkParameters("bias_affine", "t1mri_bias_corrected")

  self.linkParameters("pve_native", "grey_native" )
  self.linkParameters("pve_LDW_warped_unmodulated", "grey_native")
  self.linkParameters("pve_HDW_warped_unmodulated", "grey_HDW_warped_unmodulated")
  self.linkParameters("pve_dartel_imported", "grey_native")

  self.linkParameters("jacobian_normalized", "grey_native" )
  self.linkParameters("forward_LDW_field", "grey_native" )
  self.linkParameters("inverse_LDW_field", "grey_native" )
  self.linkParameters("forward_HDW_field", "grey_HDW_warped_unmodulated" )
  self.linkParameters("inverse_HDW_field", "grey_HDW_warped_unmodulated" )
  self.linkParameters("GM_WM_CSF_volumes_txt", "grey_native" )

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
    self.save_jacobian_normalized = False
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
  self.updateModulatedRequiredAttributes("grey")
  if self.spatial_norm == "High-dimensional: Dartel":
    self.updateSignatureFieldToShow("save_grey_modulated", "grey_HDW_warped_modulated")
  else:
    self.updateSignatureFieldToShow("save_grey_modulated", "grey_LDW_warped_modulated")

def updateSignatureAboutGreyDartel(self, proc):
  self.updateDARTELRequiredAttributes("grey")
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
  self.updateModulatedRequiredAttributes("white")
  if self.spatial_norm == "High-dimensional: Dartel":
    self.updateSignatureFieldToShow("save_white_modulated", "white_HDW_warped_modulated")
  else:
    self.updateSignatureFieldToShow("save_white_modulated", "white_LDW_warped_modulated")

def updateSignatureAboutWhiteDartel(self, proc):
  self.updateDARTELRequiredAttributes("white")
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
  self.updateModulatedRequiredAttributes("csf")
  if self.spatial_norm == "High-dimensional: Dartel":
    self.updateSignatureFieldToShow("save_csf_modulated", "csf_HDW_warped_modulated")
  else:
    self.updateSignatureFieldToShow("save_csf_modulated", "csf_LDW_warped_modulated")

def updateSignatureAboutCSFDartel(self, proc):
  self.updateDARTELRequiredAttributes("csf")
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
  self.updateDARTELRequiredAttributes("pve")
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

def updateModulatedRequiredAttributes(self, matter_key):
  if eval("self.save_" + matter_key + "_modulated") == "affine + non-linear (SPM8 default)":
    self.signature[matter_key + "_LDW_warped_modulated"].requiredAttributes["modulation"] = "affine and non-linear"
    self.signature[matter_key + "_HDW_warped_modulated"].requiredAttributes["modulation"] = "affine and non-linear"
  elif eval("self.save_" + matter_key + "_modulated") == "non-linear only":
    self.signature[matter_key + "_HDW_warped_modulated"].requiredAttributes["modulation"] = "non-linear only"
    self.signature[matter_key + "_LDW_warped_modulated"].requiredAttributes["modulation"] = "non-linear only"
  else:
    pass#grey_modulated and grey_DARTEL_modulated are hidden so...
  self.signatureChangeNotifier.notify( self )

def updateDARTELRequiredAttributes(self, matter_key):
  if eval("self.save_" + matter_key + "_dartel_imported") == "rigid (SPM8 default)":
    self.signature[matter_key + "_dartel_imported"].requiredAttributes["transformation"] = "rigid"
  elif eval("self.save_" + matter_key + "_dartel_imported") == "affine":
    self.signature[matter_key + "_dartel_imported"].requiredAttributes["transformation"] = "affine"
  else:
    pass#grey_modulated and grey_DARTEL_modulated are hidden so...
  self.signatureChangeNotifier.notify( self )

#-----------------------------------------------------------------------------------
def updateSignatureFieldToShow(self, field_to_check, field_to_modified):
  if eval("self." + field_to_check) in [False, "Neither"]:
    self.setDisable(field_to_modified)
  else:
    self.setEnable(field_to_modified)
  self.changeSignature(self.signature)
#-----------------------------------------------------------------------------------
def updateGreyNative(self, proc, dummy):
  if not None in [self.t1mri, self.TPM_template]:
    d = self.t1mri.hierarchyAttributes()
    d["processing"] = 'spm8VBMSegmentation'
    d['analysis'] = "default"
    d["template"] = self.TPM_template.hierarchyAttributes()["template"]
    return self.signature["grey_native"].findValue(d)

def updateHDWGrey(self, proc, dummy):
  if not None in [self.grey_native, self.DARTEL_template]:
    d = self.grey_native.hierarchyAttributes()
    d["template"] = self.DARTEL_template.hierarchyAttributes()["template"]
    return self.signature["grey_HDW_warped_unmodulated"].findValue(d)

def updateT1MRIBiasCorrected(self, proc, dummy):
  if self.grey_native is not None:
    d = self.grey_native.hierarchyAttributes()
    d["bias_correction_process"] = 'spm8VBMSegmentation'
    return self.signature["t1mri_bias_corrected"].findValue(d)

def updateT1MRIBiasCorrectedHDW(self, proc, dummy):
  if self.grey_HDW_warped_unmodulated is not None:
    d = self.grey_HDW_warped_unmodulated.hierarchyAttributes()
    d["bias_correction_process"] = 'spm8VBMSegmentation'
    return self.signature['bias_HDW_warped_unmodulated'].findValue(d)
  else:
    return None

def updateBatchPath(self, proc, dummy, norm):
  if self.spatial_norm == "Low-dimensional: SPM default":
    if self.grey_native is not None:
      directory_path = os.path.dirname(self.grey_native.fullPath())
      return os.path.join(directory_path, 'spm8_VBM_segmentation_job.m')
  elif self.spatial_norm == "High-dimensional: Dartel":
    if self.grey_HDW_warped_unmodulated is not None:
      directory_path = os.path.dirname(self.grey_HDW_warped_unmodulated.fullPath())
      return os.path.join(directory_path, 'spm8_VBM_segmentation_job.m')

def updateTransformMatrix(self, proc, dummy, norm):
  if self.spatial_norm == "Low-dimensional: SPM default":
    if self.grey_native is not None:
      directory_path = os.path.dirname(self.grey_native.fullPath())
      return os.path.join(directory_path, 'native_to_mni_matrix_transform.mat')
  elif self.spatial_norm == "High-dimensional: Dartel":
    if self.grey_HDW_warped_unmodulated is not None:
      directory_path = os.path.dirname(self.grey_HDW_warped_unmodulated.fullPath())
      return os.path.join(directory_path, 'native_to_mni_matrix_transform.mat')

def execution( self, context ):
  context.runProcess('SPM8VBMSegmentation_generic',
                     t1mri=self.t1mri,
                     TPM_template=self.TPM_template,
                     gaussian_classes=self.gaussian_classes,
                     bias_regulatisation=self.bias_regulatisation,
                     bias_FWHM=self.bias_FWHM,
                     affine_regularisation=self.affine_regularisation,
                     warping_regularisation=self.warping_regularisation,
                     sampling_distance=self.sampling_distance,
                     spatial_norm=self.spatial_norm,
                     DARTEL_template=self.DARTEL_template,
                     sanlm=self.sanlm,
                     mrf=self.mrf,
                     clean_up=self.clean_up,
                     print_results=self.print_results,
                     save_grey_native=self.save_grey_native,
                     grey_native=self.grey_native,
                     save_grey_normalized=self.save_grey_normalized,
                     grey_LDW_warped_unmodulated=self.grey_LDW_warped_unmodulated,
                     grey_HDW_warped_unmodulated=self.grey_HDW_warped_unmodulated,
                     save_grey_modulated=self.save_grey_modulated,
                     grey_LDW_warped_modulated=self.grey_LDW_warped_modulated,
                     grey_HDW_warped_modulated=self.grey_HDW_warped_modulated,
                     save_grey_dartel_imported=self.save_grey_dartel_imported,
                     grey_dartel_imported=self.grey_dartel_imported,
                     save_white_native=self.save_white_native,
                     white_native=self.white_native,
                     save_white_normalized=self.save_white_normalized,
                     white_LDW_warped_unmodulated=self.white_LDW_warped_unmodulated,
                     white_HDW_warped_unmodulated=self.white_HDW_warped_unmodulated,
                     save_white_modulated=self.save_white_modulated,
                     white_LDW_warped_modulated=self.white_LDW_warped_modulated,
                     white_HDW_warped_modulated=self.white_HDW_warped_modulated,
                     save_white_dartel_imported=self.save_white_dartel_imported,
                     white_dartel_imported=self.white_dartel_imported,
                     save_csf_native=self.save_csf_native,
                     csf_native=self.csf_native,
                     save_csf_normalized=self.save_csf_normalized,
                     csf_LDW_warped_unmodulated=self.csf_LDW_warped_unmodulated,
                     csf_HDW_warped_unmodulated=self.csf_HDW_warped_unmodulated,
                     save_csf_modulated=self.save_csf_modulated,
                     csf_LDW_warped_modulated=self.csf_LDW_warped_modulated,
                     csf_HDW_warped_modulated=self.csf_HDW_warped_modulated,
                     save_csf_dartel_imported=self.save_csf_dartel_imported,
                     csf_dartel_imported=self.csf_dartel_imported,
                     save_bias_native=self.save_bias_native,
                     t1mri_bias_corrected=self.t1mri_bias_corrected,
                     save_bias_normalized=self.save_bias_normalized,
                     bias_LDW_warped_unmodulated=self.bias_LDW_warped_unmodulated,
                     bias_HDW_warped_unmodulated=self.bias_HDW_warped_unmodulated,
                     save_bias_affine=self.save_bias_affine,
                     bias_affine=self.bias_affine,
                     save_pve_native=self.save_pve_native,
                     pve_native=self.pve_native,
                     save_pve_normalized=self.save_pve_normalized,
                     pve_LDW_warped_unmodulated=self.pve_LDW_warped_unmodulated,
                     pve_HDW_warped_unmodulated=self.pve_HDW_warped_unmodulated,
                     save_pve_dartel_imported=self.save_pve_dartel_imported,
                     pve_dartel_imported=self.pve_dartel_imported,
                     save_jacobian_normalized=self.save_jacobian_normalized,
                     jacobian_normalized=self.jacobian_normalized,
                     save_deformation_fields=self.save_deformation_fields,
                     forward_LDW_field=self.forward_LDW_field,
                     inverse_LDW_field=self.inverse_LDW_field,
                     forward_HDW_field=self.forward_HDW_field,
                     inverse_HDW_field=self.inverse_HDW_field,
                     DF_transformation_matrix=self.DF_transformation_matrix,
                     GM_WM_CSF_volumes_txt=self.GM_WM_CSF_volumes_txt,
                     batch_location =self.batch_location)
