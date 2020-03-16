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
from soma.spm.spm8.spatial.new_segment import NewSegment
from soma.spm.spm8.spatial.new_segment.channel import Channel
from soma.spm.spm8.spatial.new_segment.tissue import Tissue
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

userLevel = 1
name = 'spm8 - New Segment - generic'

first_channel_section = "first channel parameters"
second_channel_section = "second channel parameters"
grey_matter_section = "Grey matter"
white_matter_section = "White matter "
csf_matter_section = "CSF matter"
skull_matter_section = "Skull"
scalp_matter_section = "Scalp"
background_matter_section = "Background"
warping_section = "Warping and MRF parameters"

signature = Signature(
  't1mri', ListOf(ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image']), section=first_channel_section),
  'bias_regulatisation', Choice('no regularisation (0)',
                                'extremely light regularisation (0.00001)',
                                'very light regularisation (0.0001)',
                                'light regularisation (0.001)',
                                'medium regularisation (0.01)',
                                'heavy regularisation (0.1)',
                                'very heavy regularisation (1)',
                                'extremely heavy regularisation (10)', section=first_channel_section),
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
                      'No correction', section=first_channel_section),
  'bias_saving', Choice('save nothing',
                        'save bias corrected',
                        'save bias field',
                        'save field and corrected', section=first_channel_section),
  't1mri_bias_field', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=first_channel_section),
  't1mri_bias_corrected', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=first_channel_section),

  'second_channel', ListOf(ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image']), section=second_channel_section),
  'bias_regulatisation_2c', Choice('no regularisation (0)',
                                'extremely light regularisation (0.00001)',
                                'very light regularisation (0.0001)',
                                'light regularisation (0.001)',
                                'medium regularisation (0.01)',
                                'heavy regularisation (0.1)',
                                'very heavy regularisation (1)',
                                'extremely heavy regularisation (10)', section=second_channel_section),
  'bias_FWHM_2c', Choice('30mm cutoff',
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
                      'No correction', section=second_channel_section),
  'bias_saving_2c', Choice('save nothing',
                        'save bias corrected',
                        'save bias field',
                        'save field and corrected', section=second_channel_section),
  't1mri_bias_field_2c', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=second_channel_section),
  't1mri_bias_corrected_2c', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=second_channel_section),

  'TPM_template', ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'], section='Tissue probability map'),

  'grey_gaussian_number', Choice(1, 2, 3, 4, 5, 6, 7, 8, 'Inf', section=grey_matter_section),
  'grey_native_type', Choice("Neither", 'Native', 'DARTEL Imported', 'Native + DARTEL Imported', section=grey_matter_section),
  'grey_native', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=grey_matter_section),
  'grey_dartel_imported', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=grey_matter_section),
  'grey_warped_type', Choice("Neither", 'Modulated', 'Unmodulated', 'Modulated + Unmodulated', section=grey_matter_section),
  'grey_warped_unmodulated', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=grey_matter_section),
  'grey_warped_modulated', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=grey_matter_section),

  'white_gaussian_number', Choice(1, 2, 3, 4, 5, 6, 7, 8, 'Inf', section=white_matter_section),
  'white_native_type', Choice("Neither", 'Native', 'DARTEL Imported', 'Native + DARTEL Imported', section=white_matter_section),
  'white_native', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=white_matter_section),
  'white_dartel_imported', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=white_matter_section),
  'white_warped_type', Choice("Neither", 'Modulated', 'Unmodulated', 'Modulated + Unmodulated', section=white_matter_section),
  'white_warped_unmodulated', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=white_matter_section),
  'white_warped_modulated', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=white_matter_section),

  'csf_gaussian_number', Choice(1, 2, 3, 4, 5, 6, 7, 8, 'Inf', section=csf_matter_section),
  'csf_native_type', Choice("Neither", 'Native', 'DARTEL Imported', 'Native + DARTEL Imported', section=csf_matter_section),
  'csf_native', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=csf_matter_section),
  'csf_dartel_imported', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=csf_matter_section),
  'csf_warped_type', Choice("Neither", 'Modulated', 'Unmodulated', 'Modulated + Unmodulated', section=csf_matter_section),
  'csf_warped_unmodulated', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=csf_matter_section),
  'csf_warped_modulated', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=csf_matter_section),

  'skull_gaussian_number', Choice(1, 2, 3, 4, 5, 6, 7, 8, 'Inf', section=skull_matter_section),
  'skull_native_type', Choice("Neither", 'Native', 'DARTEL Imported', 'Native + DARTEL Imported', section=skull_matter_section),
  'skull_native', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=skull_matter_section),
  'skull_dartel_imported', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=skull_matter_section),
  'skull_warped_type', Choice("Neither", 'Modulated', 'Unmodulated', 'Modulated + Unmodulated', section=skull_matter_section),
  'skull_warped_unmodulated', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=skull_matter_section),
  'skull_warped_modulated', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=skull_matter_section),

  'scalp_gaussian_number', Choice(1, 2, 3, 4, 5, 6, 7, 8, 'Inf', section=scalp_matter_section),
  'scalp_native_type', Choice("Neither", 'Native', 'DARTEL Imported', 'Native + DARTEL Imported', section=scalp_matter_section),
  'scalp_native', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=scalp_matter_section),
  'scalp_dartel_imported', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=scalp_matter_section),
  'scalp_warped_type', Choice("Neither", 'Modulated', 'Unmodulated', 'Modulated + Unmodulated', section=scalp_matter_section),
  'scalp_warped_unmodulated', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=scalp_matter_section),
  'scalp_warped_modulated', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=scalp_matter_section),

  'background_gaussian_number', Choice(1, 2, 3, 4, 5, 6, 7, 8, 'Inf', section=background_matter_section),
  'background_native_type', Choice("Neither", 'Native', 'DARTEL Imported', 'Native + DARTEL Imported', section=background_matter_section),
  'background_native', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=background_matter_section),
  'background_dartel_imported', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=background_matter_section),
  'background_warped_type', Choice("Neither", 'Modulated', 'Unmodulated', 'Modulated + Unmodulated', section=background_matter_section),
  'background_warped_unmodulated', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=background_matter_section),
  'background_warped_modulated', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=background_matter_section),

  'mrf', Float(section=warping_section),
  'warping_regularisation',Integer(section=warping_section),
  'affine_regularisation', Choice('No Affine Registration',
                                  'ICBM space template - European brains',
                                  'ICBM space template - East Asian brains',
                                  'Average sized template',
                                  'No regularisation', section=warping_section),
  'sampling_distance', Float(section=warping_section),

  'deformation_field_type', Choice("Neither", 'Inverse', 'Forward', 'Inverse + Forward', section=warping_section),
  'forward_field', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=warping_section),
  'inverse_field', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section=warping_section),
  #'deformation_matrix', ListOf(WriteDiskItem('Matlab SPM file', 'Matlab file')),
  'seg8_mat', ListOf(WriteDiskItem('Matlab SPM file', 'Matlab file'), section="default SPM outputs"),
  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script', section="default SPM outputs"),
)

def initialization(self):
  self.setOptional("second_channel", "bias_regulatisation_2c", "bias_FWHM_2c",
                   "bias_saving_2c", "t1mri_bias_corrected_2c", "t1mri_bias_field_2c",
                   "seg8_mat")
  #Modify signature by links
  self.addLink(None, 'bias_saving', self.updateSignatureAboutFirstChannelBiasSaving)
  self.addLink(None, 'bias_saving_2c', self.updateSignatureAboutSecondChannelBiasSaving)

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

def updateSignatureAboutFirstChannelBiasSaving(self, proc):
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

def updateSignatureAboutSecondChannelBiasSaving(self, proc):
  if self.bias_saving_2c == 'save nothing':
    self.hideAndMakeOptionalSignatureFieldList(['t1mri_bias_field_2c', 't1mri_bias_corrected_2c'])
  elif self.bias_saving_2c == 'save bias corrected':
    self.hideAndMakeOptionalSignatureFieldList(['t1mri_bias_field_2c'])
    self.showAndMandadesSignatureFieldList(['t1mri_bias_corrected_2c'])
  elif self.bias_saving_2c == 'save bias field':
    self.hideAndMakeOptionalSignatureFieldList(['t1mri_bias_corrected_2c'])
    self.showAndMandadesSignatureFieldList(['t1mri_bias_field_2c'])
  elif self.bias_saving_2c == 'save field and corrected':
    self.showAndMandadesSignatureFieldList(['t1mri_bias_field_2c', 't1mri_bias_corrected_2c'])
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

def updateBatchPath(self, proc):
  if self.grey_native:
    directory_path = os.path.dirname(self.grey_native[0].fullPath())
    return os.path.join(directory_path, 'spm8_new_segment_job.m')

def execution( self, context ):
  new_segment = NewSegment()

  first_channel = Channel()

  if self.bias_regulatisation == 'no regularisation (0)':
    first_channel.unsetBiasRegularisation()
  elif self.bias_regulatisation == 'extremely light regularisation (0.00001)':
    first_channel.setBiasRegularisationToExtremelyLight()
  elif self.bias_regulatisation == 'very light regularisation (0.0001)':
    first_channel.setBiasRegularisationToVeryLight()
  elif self.bias_regulatisation == 'light regularisation (0.001)':
    first_channel.setBiasRegularisationToLight()
  elif self.bias_regulatisation == 'medium regularisation (0.01)':
    first_channel.setBiasRegularisationToMedium()
  elif self.bias_regulatisation == 'heavy regularisation (0.1)':
    first_channel.setBiasRegularisationToHeavy()
  elif self.bias_regulatisation == 'very heavy regularisation (1)':
    first_channel.setBiasRegularisationToVeryHeavy()
  elif self.bias_regulatisation == 'extremely heavy regularisation (10)':
    first_channel.setBiasRegularisationToExtremelyHeavy()
  else:
    raise ValueError('Unvalid bias_regulatisation value')

  if self.bias_FWHM == '30mm cutoff':
    first_channel.setBiasFWHMTo30cutoff()
  elif self.bias_FWHM == '40mm cutoff':
    first_channel.setBiasFWHMTo40cutoff()
  elif self.bias_FWHM == '50mm cutoff':
    first_channel.setBiasFWHMTo50cutoff()
  elif self.bias_FWHM == '60mm cutoff':
    first_channel.setBiasFWHMTo60cutoff()
  elif self.bias_FWHM == '70mm cutoff':
    first_channel.setBiasFWHMTo70cutoff()
  elif self.bias_FWHM == '80mm cutoff':
    first_channel.setBiasFWHMTo80cutoff()
  elif self.bias_FWHM == '90mm cutoff':
    first_channel.setBiasFWHMTo90cutoff()
  elif self.bias_FWHM == '100mm cutoff':
    first_channel.setBiasFWHMTo100cutoff()
  elif self.bias_FWHM == '110mm cutoff':
    first_channel.setBiasFWHMTo1100cutoff()
  elif self.bias_FWHM == '120mm cutoff':
    first_channel.setBiasFWHMTo120cutoff()
  elif self.bias_FWHM == '130mm cutoff':
    first_channel.setBiasFWHMTo130cutoff()
  elif self.bias_FWHM == '140mm cutoff':
    first_channel.setBiasFWHMTo140cutoff()
  elif self.bias_FWHM == '150mm cutoff':
    first_channel.setBiasFWHMTo150cutoff()
  elif self.bias_FWHM == 'No correction':
    first_channel.unsetBiasFWHM()
  else:
    raise ValueError('Unvalid bias_FWHM value')

  first_channel.setVolumePathList([diskitem.fullPath() for diskitem in self.t1mri])
  if self.bias_saving == 'save nothing':
    first_channel.discardBiasCorrected()
  elif self.bias_saving == 'save bias corrected':
    first_channel.saveBiasCorrected()
    first_channel.setBiasCorrectedPathList([diskitem.fullPath() for diskitem in self.t1mri_bias_corrected])
  elif self.bias_saving == 'save bias field':
    first_channel.saveBiasField()
    first_channel.setBiasFieldPath([diskitem.fullPath() for diskitem in self.t1mri_bias_field])
  elif self.bias_saving == 'save field and corrected':
    first_channel.saveBiasFieldAndBiasCorrected()
    first_channel.setBiasCorrectedPathList([diskitem.fullPath() for diskitem in self.t1mri_bias_corrected])
    first_channel.setBiasFieldPathList([diskitem.fullPath() for diskitem in self.t1mri_bias_field])
  else:
    raise ValueError('Unvalid bias_saving value')

  new_segment.appendChannel(first_channel)

  if self.second_channel:
    second_channel = Channel()

    if self.bias_regulatisation_2c == 'no regularisation (0)':
      second_channel.unsetBiasRegularisation()
    elif self.bias_regulatisation_2c == 'extremely light regularisation (0.00001)':
      second_channel.setBiasRegularisationToExtremelyLight()
    elif self.bias_regulatisation_2c == 'very light regularisation (0.0001)':
      second_channel.setBiasRegularisationToVeryLight()
    elif self.bias_regulatisation_2c == 'light regularisation (0.001)':
      second_channel.setBiasRegularisationToLight()
    elif self.bias_regulatisation_2c == 'medium regularisation (0.01)':
      second_channel.setBiasRegularisationToMedium()
    elif self.bias_regulatisation_2c == 'heavy regularisation (0.1)':
      second_channel.setBiasRegularisationToHeavy()
    elif self.bias_regulatisation_2c == 'very heavy regularisation (1)':
      second_channel.setBiasRegularisationToVeryHeavy()
    elif self.bias_regulatisation_2c == 'extremely heavy regularisation (10)':
      second_channel.setBiasRegularisationToExtremelyHeavy()
    else:
      raise ValueError('Unvalid bias_regulatisation value')

    if self.bias_FWHM_2c == '30mm cutoff':
      second_channel.setBiasFWHMTo30cutoff()
    elif self.bias_FWHM_2c == '40mm cutoff':
      second_channel.setBiasFWHMTo40cutoff()
    elif self.bias_FWHM_2c == '50mm cutoff':
      second_channel.setBiasFWHMTo50cutoff()
    elif self.bias_FWHM_2c == '60mm cutoff':
      second_channel.setBiasFWHMTo60cutoff()
    elif self.bias_FWHM_2c == '70mm cutoff':
      second_channel.setBiasFWHMTo70cutoff()
    elif self.bias_FWHM_2c == '80mm cutoff':
      second_channel.setBiasFWHMTo80cutoff()
    elif self.bias_FWHM_2c == '90mm cutoff':
      second_channel.setBiasFWHMTo90cutoff()
    elif self.bias_FWHM_2c == '100mm cutoff':
      second_channel.setBiasFWHMTo100cutoff()
    elif self.bias_FWHM_2c == '110mm cutoff':
      second_channel.setBiasFWHMTo1100cutoff()
    elif self.bias_FWHM_2c == '120mm cutoff':
      second_channel.setBiasFWHMTo120cutoff()
    elif self.bias_FWHM_2c == '130mm cutoff':
      second_channel.setBiasFWHMTo130cutoff()
    elif self.bias_FWHM_2c == '140mm cutoff':
      second_channel.setBiasFWHMTo140cutoff()
    elif self.bias_FWHM_2c == '150mm cutoff':
      second_channel.setBiasFWHMTo150cutoff()
    elif self.bias_FWHM_2c == 'No correction':
      second_channel.unsetBiasFWHM()
    else:
      raise ValueError('Unvalid bias_FWHM value')

    second_channel.setVolumePathList([diskitem.fullPath() for diskitem in self.second_channel])
    if self.bias_saving_2c == 'save nothing':
      second_channel.discardBiasCorrected()
    elif self.bias_saving_2c == 'save bias corrected':
      second_channel.saveBiasCorrected()
      second_channel.setBiasCorrectedPathList([diskitem.fullPath() for diskitem in self.t1mri_bias_corrected_2c])
    elif self.bias_saving_2c == 'save bias field':
      second_channel.saveBiasField()
      second_channel.setBiasFieldPathList([diskitem.fullPath() for diskitem in self.t1mri_bias_field_2c])
    elif self.bias_saving_2c == 'save field and corrected':
      second_channel.saveBiasFieldAndBiasCorrected()
      second_channel.setBiasCorrectedPathList([diskitem.fullPath() for diskitem in self.t1mri_bias_corrected_2c])
      second_channel.setBiasFieldPathList([diskitem.fullPath() for diskitem in self.t1mri_bias_field_2c])
    else:
      raise ValueError('Unvalid bias_saving value')

    new_segment.appendChannel(second_channel)
  else:
    pass#Second channel is optional

  new_segment.appendTissue(self.buildTissueObject('grey', 1))
  new_segment.appendTissue(self.buildTissueObject('white', 2))
  new_segment.appendTissue(self.buildTissueObject('csf', 3))
  new_segment.appendTissue(self.buildTissueObject('skull', 4))
  new_segment.appendTissue(self.buildTissueObject('scalp', 5))
  new_segment.appendTissue(self.buildTissueObject('background', 6))

  new_segment.setMRFParameter(self.mrf)

  new_segment.setWarpingRegularisation(self.warping_regularisation)

  if self.affine_regularisation == 'No Affine Registration':
    new_segment.unsetAffineRegularisation()
  elif self.affine_regularisation == 'ICBM space template - European brains':
    new_segment.setAffineRegularisationToEuropeanBrains()
  elif self.affine_regularisation == 'ICBM space template - East Asian brains':
    new_segment.setAffineRegularisationToAsianBrains()
  elif self.affine_regularisation == 'Average sized template':
    new_segment.setAffineRegularisationToAverageSizedTemplate()
  elif self.affine_regularisation == 'No regularisation':
    new_segment.unsetRegularisation()
  else:
    raise ValueError('Unvalid affine_regularisation value')

  new_segment.setSamplingDistance(self.sampling_distance)

  if self.deformation_field_type == "Neither":
    new_segment.discardDeformationField()
  elif self.deformation_field_type == 'Inverse':
    new_segment.saveDeformationFieldInverse()
    new_segment.setDeformationFieldInverseOutputPathList([diskitem.fullPath() for diskitem in self.inverse_field])
  elif self.deformation_field_type == 'Forward':
    new_segment.saveDeformationFieldForward()
    new_segment.setDeformationFieldForwardOutputPathList([diskitem.fullPath() for diskitem in self.forward_field])
  elif self.deformation_field_type == 'Inverse + Forward':
    new_segment.saveDeformationFieldInverseAndForward()
    new_segment.setDeformationFieldInverseOutputPathList([diskitem.fullPath() for diskitem in self.inverse_field])
    new_segment.setDeformationFieldForwardOutputPathList([diskitem.fullPath() for diskitem in self.forward_field])
  else:
    raise ValueError('Unvalid deformation_field_type value')

  if self.seg8_mat is not None:
    new_segment.setSeg8MatOutputPathList([diskitem.fullPath() for diskitem in self.seg8_mat])

  spm = validation()
  spm.addModuleToExecutionQueue(new_segment)
  spm.setSPMScriptPath(self.batch_location.fullPath())
  output = spm.run()
  context.log(name, html=output)


def buildTissueObject(self, tissue_name, tissue_proba_dimension):
  tissue = Tissue()

  tissue.setTissueProbilityMapPath(str(self.TPM_template.fullPath()))
  tissue.setTissueProbilityDimension(tissue_proba_dimension)

  if eval('self.' + tissue_name + '_gaussian_number') == 'Inf':
    tissue.unsetGaussian()
  else:
    tissue.setGaussianNumber(eval('self.' + tissue_name + '_gaussian_number'))

  if eval( 'self.' + tissue_name + '_native_type') == "Neither":
    tissue.unsetNativeTissue()
  elif eval( 'self.' + tissue_name + '_native_type') == 'Native':
    tissue.setNativeTissueNativeSpace()
    diskitem_list = eval('self.%s_native' % tissue_name)
    tissue.setNativeOutputPathList([diskitem.fullPath() for diskitem in diskitem_list])
  elif eval( 'self.' + tissue_name + '_native_type') == 'DARTEL Imported':
    tissue.setNativeTissueDARTELImported()
    diskitem_list = eval('self.%s_dartel_imported' % tissue_name)
    tissue.setDartelOutputPathList([diskitem.fullPath() for diskitem in diskitem_list])
  elif eval( 'self.' + tissue_name + '_native_type') == 'Native + DARTEL Imported':
    tissue.setNativeTissueNativeSpaceAndDARTELImported()
    diskitem_list = eval('self.%s_native' % tissue_name)
    tissue.setNativeOutputPathList([diskitem.fullPath() for diskitem in diskitem_list])
    diskitem_list = eval('self.%s_dartel_imported' % tissue_name)
    tissue.setDartelOutputPathList([diskitem.fullPath() for diskitem in diskitem_list])
  else:
    raise ValueError('Unvalid choice for ' + tissue_name + '_native_type')

  if eval( 'self.' + tissue_name + '_warped_type') == "Neither":
    tissue.unsetWarpedTissue()
  elif eval( 'self.' + tissue_name + '_warped_type') == 'Modulated':
    tissue.setWarpedTissueModulated()
    diskitem_list = eval('self.%s_warped_modulated' % tissue_name)
    tissue.setWarpedModulatedOutputPathList([diskitem.fullPath() for diskitem in diskitem_list])
  elif eval( 'self.' + tissue_name + '_warped_type') == 'Unmodulated':
    tissue.setWarpedTissueUnmodulated()
    diskitem_list = eval('self.%s_warped_unmodulated' % tissue_name)
    tissue.setWarpedUnmodulatedOutputPathList([diskitem.fullPath() for diskitem in diskitem_list])
  elif eval( 'self.' + tissue_name + '_warped_type') == 'Modulated + Unmodulated':
    tissue.setWarpedTissueModulatedAndUnmodulated()
    diskitem_list = eval('self.%s_warped_modulated' % tissue_name)
    tissue.setWarpedModulatedOutputPathList([diskitem.fullPath() for diskitem in diskitem_list])
    diskitem_list = eval('self.%s_warped_unmodulated' % tissue_name)
    tissue.setWarpedUnmodulatedOutputPathList([diskitem.fullPath() for diskitem in diskitem_list])
  else:
    raise ValueError('Unvalid choice for ' + tissue_name + '_warped_type')

  return tissue


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

