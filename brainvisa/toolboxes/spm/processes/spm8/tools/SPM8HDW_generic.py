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
from soma.spm.spm8.tools.hdw import HDW
from soma.spm.spm8.tools.hdw.subject import Subject
from soma.spm.spm8.tools.hdw.bias_correction_options import BiasCorrectionOptions
from soma.spm.spm8.tools.hdw.warping_options import WarpingOptions
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
name = 'spm8 - High-Dimensional Warping - generic'

bias_correction_section = "Bias correction options"
warping_section = "warping options"

signature = Signature(
  "reference", ReadDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image']),
  "moved", ReadDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image']),
  "bias_iteration", Integer(),
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
                      section=bias_correction_section),
  'bias_regulatisation', Choice('no regularisation (0)',
                                'extremely light regularisation (1e-09)',
                                'very light regularisation (1e-08)',
                                'light regularisation (1e-07)',
                                'medium regularisation (1e-06)',
                                'heavy regularisation (1e-05)',
                                'very heavy regularisation (0.0001)',
                                'extremely heavy regularisation (0.001)',
                                section=bias_correction_section),
  'lm_regulatisation', Choice('no regularisation (0)',
                              'extremely light regularisation (1e-09)',
                              'very light regularisation (1e-08)',
                              'light regularisation (1e-07)',
                              'medium regularisation (1e-06)',
                              'heavy regularisation (1e-05)',
                              'very heavy regularisation (0.0001)',
                              'extremely heavy regularisation (0.001)',
                              section=bias_correction_section),
  "warping_iteration", Integer(section=warping_section),
  "warping_regularisation", Float(section=warping_section),
  "custom_outputs", Boolean(section='outputs'),
  "deformation_field", WriteDiskItem("4D Volume", ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section='outputs'),
  "jacobian_determinant", WriteDiskItem("4D Volume", ["gz compressed NIFTI-1 image", "NIFTI-1 image"], section='outputs'),

  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script', section='default SPM outputs' ),
)
def initialization(self):

  self.addLink(None, "custom_outputs", self.updateSignatureAboutCustomOutputs)

  self.addLink("batch_location", "deformation_field", self.updateBatchPath)

  #SPM default initialisation
  self.bias_iteration = 8
  self.bias_FWHM = '60mm cutoff'
  self.bias_regulatisation = 'medium regularisation (1e-06)'
  self.lm_regulatisation = 'medium regularisation (1e-06)'
  self.warping_iteration = 8
  self.warping_regularisation = 4

  self.custom_outputs = False

def updateSignatureAboutCustomOutputs(self, proc):
  if self.custom_outputs:
    self.setEnable("deformation_field")
    self.setEnable("jacobian_determinant", mandatory=False)
  else:
    self.setDisable("deformation_field", "jacobian_determinant")
  self.signatureChangeNotifier.notify( self )

def updateBatchPath(self, proc):
  if self.deformation_field is not None:
    directory_path = os.path.dirname(self.deformation_field.fullPath())
    return os.path.join(directory_path, 'spm8_hdw_job.m')

def execution( self, context ):
  hdw = HDW()
  subject = Subject()
  subject.setReferenceImage(self.reference.fullPath())
  subject.setMovedImage(self.moved.fullPath())
  if self.custom_outputs:
    subject.setOutputDeformationFieldPath(self.deformation_field.fullPath())
    if self.jacobian_determinant is not None:
      subject.setOutputJacobianDeterminantPath(self.jacobian_determinant.fullPath())
    else:
      pass#default SPM path used
  else:
    pass#default SPM path used
  hdw.appendSubject(subject)

  bias_correction = BiasCorrectionOptions()
  bias_correction.setIterations(self.bias_iteration)
  if self.bias_FWHM == "30mm cutoff":
    bias_correction.setBiasFWHMTo30mmCutoff()
  elif self.bias_FWHM == "40mm cutoff":
    bias_correction.setBiasFWHMTo40mmCutoff()
  elif self.bias_FWHM == "50mm cutoff":
    bias_correction.setBiasFWHMTo50mmCutoff()
  elif self.bias_FWHM == "60mm cutoff":
    bias_correction.setBiasFWHMTo60mmCutoff()
  elif self.bias_FWHM == "70mm cutoff":
    bias_correction.setBiasFWHMTo70mmCutoff()
  elif self.bias_FWHM == "80mm cutoff":
    bias_correction.setBiasFWHMTo80mmCutoff()
  elif self.bias_FWHM == "90mm cutoff":
    bias_correction.setBiasFWHMTo90mmCutoff()
  elif self.bias_FWHM == "100mm cutoff":
    bias_correction.setBiasFWHMTo100mmCutoff()
  elif self.bias_FWHM == "110mm cutoff":
    bias_correction.setBiasFWHMTo110mmCutoff()
  elif self.bias_FWHM == "120mm cutoff":
    bias_correction.setBiasFWHMTo120mmCutoff()
  elif self.bias_FWHM == "130mm cutoff":
    bias_correction.setBiasFWHMTo130mmCutoff()
  elif self.bias_FWHM == "140mm cutoff":
    bias_correction.setBiasFWHMTo140mmCutoff()
  elif self.bias_FWHM == "150mm cutoff":
    bias_correction.setBiasFWHMTo150mmCutoff()
  elif self.bias_FWHM == "No correction":
    bias_correction.unsetBiasFWHM()
  else:
    raise ValueError("Unvalid bias_correction")

  if self.bias_regulatisation == 'no regularisation (0)':
    bias_correction.unsetBiasRegularisation()
  elif self.bias_regulatisation == 'extremely light regularisation (1e-09)':
    bias_correction.setBiasRegularisationToExtremelyLight()
  elif self.bias_regulatisation == 'very light regularisation (1e-08)':
    bias_correction.setBiasRegularisationToVeryLight()
  elif self.bias_regulatisation == 'light regularisation (1e-07)':
    bias_correction.setBiasRegularisationToLight()
  elif self.bias_regulatisation == 'medium regularisation (1e-06)':
    bias_correction.setBiasRegularisationToMedium()
  elif self.bias_regulatisation == 'heavy regularisation (1e-05)':
    bias_correction.setBiasRegularisationToHeavy()
  elif self.bias_regulatisation == 'very heavy regularisation (0.0001)':
    bias_correction.setBiasRegularisationToVeryHeavy()
  elif self.bias_regulatisation == 'extremely heavy regularisation (0.001)':
    bias_correction.setBiasRegularisationToExtremelyHeavy()
  else:
    raise ValueError('Unvalid bias_regulatisation value')

  if self.lm_regulatisation == 'no regularisation (0)':
    bias_correction.unsetLMRegularisation()
  elif self.lm_regulatisation == 'extremely light regularisation (1e-09)':
    bias_correction.setLMRegularisationToExtremelyLight()
  elif self.lm_regulatisation == 'very light regularisation (1e-08)':
    bias_correction.setLMRegularisationToVeryLight()
  elif self.lm_regulatisation == 'light regularisation (1e-07)':
    bias_correction.setLMRegularisationToLight()
  elif self.lm_regulatisation == 'medium regularisation (1e-06)':
    bias_correction.setLMRegularisationToMedium()
  elif self.lm_regulatisation == 'heavy regularisation (1e-05)':
    bias_correction.setLMRegularisationToHeavy()
  elif self.lm_regulatisation == 'very heavy regularisation (0.0001)':
    bias_correction.setLMRegularisationToVeryHeavy()
  elif self.lm_regulatisation == 'extremely heavy regularisation (0.001)':
    bias_correction.setLMRegularisationToExtremelyHeavy()
  else:
    raise ValueError('Unvalid bias_regulatisation value')

  hdw.replaceBiasCorrectionOptions(bias_correction)

  warping = WarpingOptions()
  warping.setIterations(self.warping_iteration)
  warping.setWarpingRegularisation(self.warping_regularisation)

  hdw.replaceWarpingOptions(warping)

  spm = validation()
  spm.addModuleToExecutionQueue(hdw)
  spm.setSPMScriptPath(self.batch_location.fullPath())
  output = spm.run()
  context.log(name, html=output)
