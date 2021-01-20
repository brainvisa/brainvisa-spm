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
import os
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
#------------------------------------------------------------------------------

userLevel = 0
name = "spm8 - New Segment"

channel_section = "Channel parameters"
grey_matter_section = "Grey matter"
white_matter_section = "White matter "
csf_matter_section = "CSF matter"
skull_matter_section = "Skull"
scalp_matter_section = "Scalp"
background_matter_section = "Background"
warping_section = "Warping and MRF parameters"

signature = Signature(
  't1mri', ReadDiskItem('Raw T1 MRI', 'NIFTI-1 image', section=channel_section),
  'TPM_template', ReadDiskItem('TPM template', ['NIFTI-1 image', 'SPM image', 'MINC image'], section=channel_section),
  'bias_regulatisation', Choice('no regularisation (0)',
                                'extremely light regularisation (0.00001)',
                                'very light regularisation (0.0001)',
                                'light regularisation (0.001)',
                                'medium regularisation (0.01)',
                                'heavy regularisation (0.1)',
                                'very heavy regularisation (1)',
                                'extremely heavy regularisation (10)',
                                section=channel_section),
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
                      section=channel_section),
  'bias_saving', Choice('save nothing',
                        'save bias corrected',
                        'save bias field',
                        'save field and corrected',
                        section=channel_section),
  't1mri_bias_field', WriteDiskItem('T1 MRI Bias field', ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section=channel_section ),
  't1mri_bias_corrected',
  WriteDiskItem('T1 MRI Bias Corrected', ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'transformation':'none',
                                    'warping_method':'none'},
                section=channel_section),
  #GREY CLASS
  'grey_gaussian_number', Choice(1, 2, 3, 4, 5, 6, 7, 8, 'Inf', section=grey_matter_section),
  'grey_native_type', Choice("Neither", 'Native', 'DARTEL Imported', 'Native + DARTEL Imported', section=grey_matter_section),
  'grey_native',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'grey',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=grey_matter_section),
  'grey_dartel_imported',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'grey',
                                    'transformation':'rigid',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=grey_matter_section),
  'grey_warped_type', Choice("Neither", 'Modulated', 'Unmodulated', 'Modulated + Unmodulated', section=grey_matter_section),
  'grey_warped_unmodulated',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'grey',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'low-dimensional'},
                section=grey_matter_section),
  'grey_warped_modulated',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes = {'tissue_class':'grey',
                                      'transformation':'none',
                                      'modulation':'affine and non-linear',
                                      'warping_method':'low-dimensional'},
                section=grey_matter_section),
  #WHITE CLASS
  'white_gaussian_number', Choice(1, 2, 3, 4, 5, 6, 7, 8, 'Inf', section=white_matter_section),
  'white_native_type', Choice("Neither", 'Native', 'DARTEL Imported', 'Native + DARTEL Imported', section=white_matter_section),
  'white_native',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'white',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=white_matter_section),
  'white_dartel_imported',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'white',
                                    'transformation':'rigid',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=white_matter_section),
  'white_warped_type', Choice("Neither", 'Modulated', 'Unmodulated', 'Modulated + Unmodulated', section=white_matter_section),
  'white_warped_unmodulated',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'white',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'low-dimensional'},
                section=white_matter_section),
  'white_warped_modulated',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'white',
                                    'transformation':'none',
                                    'modulation':'affine and non-linear',
                                    'warping_method':'low-dimensional'},
                section=white_matter_section),
  #CSF CLASS
  'csf_gaussian_number', Choice(1, 2, 3, 4, 5, 6, 7, 8, 'Inf', section=csf_matter_section),
  'csf_native_type', Choice("Neither", 'Native', 'DARTEL Imported', 'Native + DARTEL Imported', section=csf_matter_section),
  'csf_native',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'csf',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=csf_matter_section),
  'csf_dartel_imported',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'csf',
                                    'transformation':'rigid',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=csf_matter_section),
  'csf_warped_type', Choice("Neither", 'Modulated', 'Unmodulated', 'Modulated + Unmodulated', section=csf_matter_section),
  'csf_warped_unmodulated',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'csf',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'low-dimensional'},
                section=csf_matter_section),
  'csf_warped_modulated',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'csf',
                                    'transformation':'none',
                                    'modulation':'affine and non-linear',
                                    'warping_method':'low-dimensional'},
                section=csf_matter_section),
  #SKULL CLASS
  'skull_gaussian_number', Choice(1, 2, 3, 4, 5, 6, 7, 8, 'Inf', section=skull_matter_section),
  'skull_native_type', Choice("Neither", 'Native', 'DARTEL Imported', 'Native + DARTEL Imported', section=skull_matter_section),
  'skull_native',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'skull',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=skull_matter_section),
  'skull_dartel_imported',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'skull',
                                    'transformation':'rigid',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=skull_matter_section),
  'skull_warped_type', Choice("Neither", 'Modulated', 'Unmodulated', 'Modulated + Unmodulated', section=skull_matter_section),
  'skull_warped_unmodulated',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'skull',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'low-dimensional'},
                section=skull_matter_section),
  'skull_warped_modulated',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'skull',
                                    'transformation':'none',
                                    'modulation':'affine and non-linear',
                                    'warping_method':'low-dimensional'},
                section=skull_matter_section),
  #SCALP CLASS
  'scalp_gaussian_number', Choice(1, 2, 3, 4, 5, 6, 7, 8, 'Inf', section=scalp_matter_section),
  'scalp_native_type', Choice("Neither", 'Native', 'DARTEL Imported', 'Native + DARTEL Imported', section=scalp_matter_section),
  'scalp_native',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'scalp',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=scalp_matter_section),
  'scalp_dartel_imported',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'scalp',
                                    'transformation':'rigid',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=scalp_matter_section),
  'scalp_warped_type', Choice("Neither", 'Modulated', 'Unmodulated', 'Modulated + Unmodulated', section=scalp_matter_section),
  'scalp_warped_unmodulated',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'scalp',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'low-dimensional'},
                section=scalp_matter_section),
  'scalp_warped_modulated',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'scalp',
                                    'transformation':'none',
                                    'modulation':'affine and non-linear',
                                    'warping_method':'low-dimensional'},
                section=scalp_matter_section),
  #BACKGROUND CLASS
  'background_gaussian_number', Choice(1, 2, 3, 4, 5, 6, 7, 8, 'Inf', section=background_matter_section),
  'background_native_type', Choice("Neither", 'Native', 'DARTEL Imported', 'Native + DARTEL Imported', section=background_matter_section),
  'background_native',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'none',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=background_matter_section),
  'background_dartel_imported',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'none',
                                    'transformation':'rigid',
                                    'modulation':'none',
                                    'warping_method':'none'},
                section=background_matter_section),
  'background_warped_type', Choice("Neither", 'Modulated', 'Unmodulated', 'Modulated + Unmodulated', section=background_matter_section),
  'background_warped_unmodulated',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'none',
                                    'transformation':'none',
                                    'modulation':'none',
                                    'warping_method':'low-dimensional'},
                section=background_matter_section),
  'background_warped_modulated',
  WriteDiskItem('T1 MRI tissue probability map',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes={'tissue_class':'none',
                                    'transformation':'none',
                                    'modulation':'affine and non-linear',
                                    'warping_method':'low-dimensional'},
                section=background_matter_section),
  'mrf', Float(section=warping_section),
  'warping_regularisation',Integer(section=warping_section),
  'affine_regularisation', Choice('No Affine Registration',
                                  'ICBM space template - European brains',
                                  'ICBM space template - East Asian brains',
                                  'Average sized template',
                                  'No regularisation',
                                  section=warping_section),
  'sampling_distance', Float(section=warping_section),

  'deformation_field_type', Choice("Neither", 'Inverse', 'Forward', 'Inverse + Forward', section=warping_section),
  'forward_field',
  WriteDiskItem('SPM deformation field',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes = {'direction':'forward',
                                      'warping_method':'low-dimensional'},
                section=warping_section),
  'inverse_field',
  WriteDiskItem('SPM deformation field',
                ["gz compressed NIFTI-1 image", "NIFTI-1 image"],
                requiredAttributes = {'direction':'inverse',
                                      'warping_method':'low-dimensional'},
                section=warping_section),
  #'deformation_matrix', WriteDiskItem('Matlab SPM file', 'Matlab file'),
  'seg8_mat', WriteDiskItem('Matlab SPM file', 'Matlab file', section='default SPM outputs'),

  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script', section='default SPM outputs'),
)

def initialization(self):
  #Modify signature by links
  self.addLink(None, 'bias_saving', self.updateSignatureAboutBiasSaving)

  self.addLink(None, 'grey_native_type', self.updateSignatureAboutGreyNativeType)
  self.addLink(None, 'white_native_type', self.updateSignatureAboutWhiteNativeType)
  self.addLink(None, 'csf_native_type', self.updateSignatureAboutCSFNativeType)
  self.addLink(None, 'skull_native_type', self.updateSignatureAboutSkullNativeType)
  self.addLink(None, 'scalp_native_type', self.updateSignatureAboutScalpNativeType)
  self.addLink(None, 'background_native_type', self.updateSignatureAboutBackgroundNativeType)

  self.addLink(None, 'grey_warped_type', self.updateSignatureAboutGreyWarpedType)
  self.addLink(None, 'white_warped_type', self.updateSignatureAboutWhiteWarpedType)
  self.addLink(None, 'csf_warped_type', self.updateSignatureAboutCSFWarpedType)
  self.addLink(None, 'skull_warped_type', self.updateSignatureAboutSkullWarpedType)
  self.addLink(None, 'scalp_warped_type', self.updateSignatureAboutScalpWarpedType)
  self.addLink(None, 'background_warped_type', self.updateSignatureAboutBackgroundWarpedType)

  self.addLink(None, 'deformation_field_type', self.updateSignatureAboutDeformationField)

  self.addLink("batch_location", "grey_native", self.updateBatchPath)
  self.addLink("seg8_mat", "t1mri_bias_corrected", self.updateSeg8Path)

  self.linkParameters('t1mri_bias_corrected', ('t1mri', 'TPM_template'), self.updateT1MRIBiasCorrected)
  self.linkParameters('t1mri_bias_field', 't1mri_bias_corrected')
  self.linkParameters('grey_native', ('t1mri', 'TPM_template'), self.updateGreyNative)
  self.linkParameters('grey_dartel_imported', 'grey_native')
  self.linkParameters('grey_warped_unmodulated', 'grey_native')
  self.linkParameters('grey_warped_modulated', 'grey_native')

  self.linkParameters('white_native', 'grey_native')
  self.linkParameters('white_dartel_imported', 'grey_native')
  self.linkParameters('white_warped_unmodulated', 'grey_native')
  self.linkParameters('white_warped_modulated', 'grey_native')

  self.linkParameters('csf_native', 'grey_native')
  self.linkParameters('csf_dartel_imported', 'grey_native')
  self.linkParameters('csf_warped_unmodulated', 'grey_native')
  self.linkParameters('csf_warped_modulated', 'grey_native')

  self.linkParameters('skull_native', 'grey_native')
  self.linkParameters('skull_dartel_imported', 'grey_native')
  self.linkParameters('skull_warped_unmodulated', 'grey_native')
  self.linkParameters('skull_warped_modulated', 'grey_native')

  self.linkParameters('scalp_native', 'grey_native')
  self.linkParameters('scalp_dartel_imported', 'grey_native')
  self.linkParameters('scalp_warped_unmodulated', 'grey_native')
  self.linkParameters('scalp_warped_modulated', 'grey_native')

  self.linkParameters('background_native', 'grey_native')
  self.linkParameters('background_dartel_imported', 'grey_native')
  self.linkParameters('background_warped_unmodulated', 'grey_native')
  self.linkParameters('background_warped_modulated', 'grey_native')


  self.linkParameters('forward_field', 'grey_native')
  self.linkParameters('inverse_field', 'grey_native')

  #SPM default initialisation
  self.bias_regulatisation = 'very light regularisation (0.0001)'
  self.bias_FWHM = '60mm cutoff'
  self.bias_saving = 'save nothing'

  self.grey_gaussian_number = 2
  self.grey_native_type = 'Native'
  self.grey_warped_type = "Neither"

  self.white_gaussian_number = 2
  self.white_native_type = 'Native'
  self.white_warped_type = "Neither"

  self.csf_gaussian_number = 2
  self.csf_native_type = 'Native'
  self.csf_warped_type = "Neither"

  self.skull_gaussian_number = 3
  self.skull_native_type = 'Native'
  self.skull_warped_type = "Neither"

  self.scalp_gaussian_number = 4
  self.scalp_native_type = 'Native'
  self.scalp_warped_type = "Neither"

  self.background_gaussian_number = 2
  self.background_native_type = "Neither"
  self.background_warped_type = "Neither"

  self.mrf = 0
  self.warping_regularisation = 4
  self.affine_regularisation = 'ICBM space template - European brains'
  self.sampling_distance = 3
  self.deformation_field_type = "Neither"

def updateSignatureAboutBiasSaving(self, proc):
  if self.bias_saving == 'save nothing':
    self.hideAndMakeOptionalSignatureFieldList(['t1mri_bias_field', 't1mri_bias_corrected'])
  elif self.bias_saving == 'save bias corrected':
    self.hideAndMakeOptionalSignatureFieldList(['t1mri_bias_field'])
    self.showAndMandadesSignatureFieldList(['t1mri_bias_corrected'])
  elif self.bias_saving == 'save bias field':
    self.hideAndMakeOptionalSignatureFieldList(['t1mri_bias_corrected'])
    self.showAndMandadesSignatureFieldList(['t1mri_bias_field'])
  elif self.bias_saving == 'save field and corrected':
    self.showAndMandadesSignatureFieldList(['t1mri_bias_field', 't1mri_bias_corrected'])
  self.changeSignature(self.signature)

def updateSignatureAboutGreyNativeType(self, proc):
  self._updateSignatureAboutNativeType('grey')

def updateSignatureAboutWhiteNativeType(self, proc):
  self._updateSignatureAboutNativeType('white')

def updateSignatureAboutCSFNativeType(self, proc):
  self._updateSignatureAboutNativeType('csf')

def updateSignatureAboutSkullNativeType(self, proc):
  self._updateSignatureAboutNativeType('skull')

def updateSignatureAboutScalpNativeType(self, proc):
  self._updateSignatureAboutNativeType('scalp')

def updateSignatureAboutBackgroundNativeType(self, proc):
  self._updateSignatureAboutNativeType('background')

def _updateSignatureAboutNativeType(self, tissue_name):
  native_type = eval('self.' + tissue_name + '_native_type')
  if native_type == "Neither":
    self.hideAndMakeOptionalSignatureFieldList([tissue_name + '_native', tissue_name + '_dartel_imported'])
  elif native_type == 'Native':
    self.showAndMandadesSignatureFieldList([tissue_name + '_native'])
    self.hideAndMakeOptionalSignatureFieldList([tissue_name + '_dartel_imported'])
  elif native_type == 'DARTEL Imported':
    self.showAndMandadesSignatureFieldList([tissue_name + '_dartel_imported'])
    self.hideAndMakeOptionalSignatureFieldList([tissue_name + '_native'])
  elif native_type == 'Native + DARTEL Imported':
    self.showAndMandadesSignatureFieldList([tissue_name + '_native', tissue_name + '_dartel_imported'])

def updateSignatureAboutGreyWarpedType(self, proc):
  self._updateSignatureAboutWarpedType('grey')

def updateSignatureAboutWhiteWarpedType(self, proc):
  self._updateSignatureAboutWarpedType('white')

def updateSignatureAboutCSFWarpedType(self, proc):
  self._updateSignatureAboutWarpedType('csf')

def updateSignatureAboutSkullWarpedType(self, proc):
  self._updateSignatureAboutWarpedType('skull')

def updateSignatureAboutScalpWarpedType(self, proc):
  self._updateSignatureAboutWarpedType('scalp')

def updateSignatureAboutBackgroundWarpedType(self, proc):
  self._updateSignatureAboutWarpedType('background')

def _updateSignatureAboutWarpedType(self, tissue_name):
  native_type = eval('self.' + tissue_name + '_warped_type')
  if native_type == "Neither":
    self.hideAndMakeOptionalSignatureFieldList([tissue_name + '_warped_unmodulated', tissue_name + '_warped_modulated'])
  elif native_type == 'Modulated':
    self.showAndMandadesSignatureFieldList([tissue_name + '_warped_modulated'])
    self.hideAndMakeOptionalSignatureFieldList([tissue_name + '_warped_unmodulated'])
  elif native_type == 'Unmodulated':
    self.showAndMandadesSignatureFieldList([tissue_name + '_warped_unmodulated'])
    self.hideAndMakeOptionalSignatureFieldList([tissue_name + '_warped_modulated'])
  elif native_type == 'Modulated + Unmodulated':
    self.showAndMandadesSignatureFieldList([tissue_name + '_warped_modulated', tissue_name + '_warped_unmodulated'])

def updateSignatureAboutDeformationField(self, proc):
  if self.deformation_field_type == "Neither":
    self.hideAndMakeOptionalSignatureFieldList(['forward_field', 'inverse_field'])
  elif self.deformation_field_type == 'Inverse':
    self.hideAndMakeOptionalSignatureFieldList(['forward_field'])
    self.showAndMandadesSignatureFieldList(['inverse_field'])
  elif self.deformation_field_type == 'Forward':
    self.hideAndMakeOptionalSignatureFieldList(['inverse_field'])
    self.showAndMandadesSignatureFieldList(['forward_field'])
  elif self.deformation_field_type == 'Inverse + Forward':
    self.showAndMandadesSignatureFieldList(['forward_field', 'inverse_field'])

def updateT1MRIBiasCorrected(self, proc, dummy):
  if not None in [self.t1mri, self.TPM_template]:
    attr = self.t1mri.hierarchyAttributes()
    d = {"_database": attr["_database"]}
    d["center"] = attr["center"]
    d["subject"] = attr["subject"]
    d["acquisition"] = attr["acquisition"]
    d['processing'] = 'spm8NewSegment'
    d['bias_correction_process'] = 'spm8NewSegment'
    d['analysis'] = "default"
    d['template'] = self.TPM_template.hierarchyAttributes()['template']
    return self.signature['t1mri_bias_corrected'].findValue(d)

def updateGreyNative(self, proc, dummy):
  if not None in [self.t1mri, self.TPM_template]:
    d = self.t1mri.hierarchyAttributes()
    d['processing'] = 'spm8NewSegment'
    d['bias_correction_process'] = 'spm8NewSegment'
    d['analysis'] = "default"
    d['template'] = self.TPM_template.hierarchyAttributes()['template']
    return self.signature['grey_native'].findValue(d)

def updateBatchPath(self, proc):
  if self.grey_native is not None:
    directory_path = os.path.dirname(self.grey_native.fullPath())
    return os.path.join(directory_path, 'spm8_new_segment_job.m')

def updateSeg8Path(self, proc):
  if self.t1mri_bias_corrected is not None:
    t1mri_bias_corrected_name = self.t1mri_bias_corrected.fullName()
    return t1mri_bias_corrected_name + "_seg8.mat"

def execution( self, context ):
  context.runProcess('SPM8NewSegment_generic',
                     t1mri=self.t1mri,
                     TPM_template=self.TPM_template,
                     bias_regulatisation=self.bias_regulatisation,
                     bias_FWHM=self.bias_FWHM,
                     bias_saving=self.bias_saving,
                     t1mri_bias_field=self.t1mri_bias_field,
                     t1mri_bias_corrected=self.t1mri_bias_corrected,
                     grey_gaussian_number=self.grey_gaussian_number,
                     grey_native_type=self.grey_native_type,
                     grey_native=self.grey_native,
                     grey_dartel_imported=self.grey_dartel_imported,
                     grey_warped_type=self.grey_warped_type,
                     grey_warped_unmodulated=self.grey_warped_unmodulated,
                     grey_warped_modulated=self.grey_warped_modulated,
                     white_gaussian_number=self.white_gaussian_number,
                     white_native_type=self.white_native_type,
                     white_native=self.white_native,
                     white_dartel_imported=self.white_dartel_imported,
                     white_warped_type=self.white_warped_type,
                     white_warped_unmodulated=self.white_warped_unmodulated,
                     white_warped_modulated=self.white_warped_modulated,
                     csf_gaussian_number=self.csf_gaussian_number,
                     csf_native_type=self.csf_native_type,
                     csf_native=self.csf_native,
                     csf_dartel_imported=self.csf_dartel_imported,
                     csf_warped_type=self.csf_warped_type,
                     csf_warped_unmodulated=self.csf_warped_unmodulated,
                     csf_warped_modulated=self.csf_warped_modulated,
                     skull_gaussian_number=self.skull_gaussian_number,
                     skull_native_type=self.skull_native_type,
                     skull_native=self.skull_native,
                     skull_dartel_imported=self.skull_dartel_imported,
                     skull_warped_type=self.skull_warped_type,
                     skull_warped_unmodulated=self.skull_warped_unmodulated,
                     skull_warped_modulated=self.skull_warped_modulated,
                     scalp_gaussian_number=self.scalp_gaussian_number,
                     scalp_native_type=self.scalp_native_type,
                     scalp_native=self.scalp_native,
                     scalp_dartel_imported=self.scalp_dartel_imported,
                     scalp_warped_type=self.scalp_warped_type,
                     scalp_warped_unmodulated=self.scalp_warped_unmodulated,
                     scalp_warped_modulated=self.scalp_warped_modulated,
                     background_gaussian_number=self.background_gaussian_number,
                     background_native_type=self.background_native_type,
                     background_native=self.background_native,
                     background_dartel_imported=self.background_dartel_imported,
                     background_warped_type=self.background_warped_type,
                     background_warped_unmodulated=self.background_warped_unmodulated,
                     background_warped_modulated=self.background_warped_modulated,
                     mrf=self.mrf,
                     warping_regularisation=self.warping_regularisation,
                     affine_regularisation=self.affine_regularisation,
                     sampling_distance=self.sampling_distance,
                     deformation_field_type=self.deformation_field_type,
                     forward_field=self.forward_field,
                     inverse_field=self.inverse_field,
                     seg8_mat=self.seg8_mat,
                     batch_location=self.batch_location)

#===============================================================================
#
#===============================================================================
def showAndMandadesSignatureFieldList(self, field_list):
  for field in field_list:
    self.signature[field].userLevel = 0
    self.signature[field].mandatory = True
  self.changeSignature(self.signature)

def hideAndMakeOptionalSignatureFieldList(self, field_list):
  for field in field_list:
    self.signature[field].userLevel = 3
    self.signature[field].mandatory = False
  self.changeSignature(self.signature)

