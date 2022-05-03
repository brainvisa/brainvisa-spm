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
from soma.spm.spm12.tools.longitudinal_registration.serial import SerialLongitudinalRegistration
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

userLevel = 1
name = 'spm12 - serial longitudinal registration - generic'


signature = Signature(
  'volumes', ListOf(ReadDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"])),
  'times', ListOf(Float()),
  'noise_estimate', Choice("NaN", "Scalar", "Matrix"),
  'noise_estimate_value', Matrix(),
  'warping_regularisation', ListOf(Float()),
  'bias_regularisation', Float(),
  'customs_outputs', Boolean(),
  'save_MPA', Boolean(),
  'MPA', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]),
  'save_jacobians', Boolean(),
  'jacobians',ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"])),
  'save_divergences', Boolean(),
  'divergences',ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"])),
  'save_deformation_fields', Boolean(),
  'deformation_fields', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"])),
  'batch_location', WriteDiskItem('Matlab SPM script', 'Matlab script', section='default SPM outputs')
)

def initialization(self):
  self.addLink(None, "noise_estimate", self.updateSignatureAboutNoise)
  self.addLink(None, "save_MPA", self.updateSignatureAboutMPA)
  self.addLink(None, "customs_outputs", self.updateSignatureAboutMPA)
  self.addLink(None, "save_jacobians", self.updateSignatureAboutJacobians)
  self.addLink(None, "customs_outputs", self.updateSignatureAboutJacobians)
  self.addLink(None, "save_divergences", self.updateSignatureAboutDivergences)
  self.addLink(None, "customs_outputs", self.updateSignatureAboutDivergences)
  self.addLink(None, "save_deformation_fields", self.updateSignatureAboutDeformationField)
  self.addLink(None, "customs_outputs", self.updateSignatureAboutDeformationField)
  self.addLink("batch_location", "volumes", self.updateBatchPath)

  #SPM default initialisation
  self.time_difference = [1]
  self.noise_estimate = "NaN"
  self.warping_regularisation = [0, 0, 100, 25, 100]
  self.bias_regularisation = 1000000
  self.save_MPA = True
  self.save_jacobians = False
  self.save_divergences = True
  self.save_deformation_fields = False

def updateSignatureAboutNoise(self, proc):
  if self.noise_estimate == "NaN":
    self.setDisable("noise_estimate_value")
  elif self.noise_estimate in ["Scalar", "Matrix"]:
    self.setEnable("noise_estimate_value")
  else:
    raise ValueError("Unvalid noise_estimate")
  self.changeSignature(self.signature)

def updateSignatureAboutMPA(self, proc):
  if self.save_MPA and self.customs_outputs:
    self.setEnable("MPA")
  else:
    self.setDisable("MPA")
  self.changeSignature(self.signature)

def updateSignatureAboutJacobians(self, proc):
  if self.save_jacobians and self.customs_outputs:
    self.setEnable("jacobians")
  else:
    self.setDisable("jacobians")
  self.changeSignature(self.signature)

def updateSignatureAboutDivergences(self, proc):
  if self.save_divergences and self.customs_outputs:
    self.setEnable("divergences")
  else:
    self.setDisable("divergences")
  self.changeSignature(self.signature)

def updateSignatureAboutDeformationField(self, proc):
  if self.save_deformation_fields and self.customs_outputs:
    self.setEnable("deformation_fields")
  else:
    self.setDisable("deformation_fields")
  self.changeSignature(self.signature)

def updateBatchPath(self, proc):
  if self.volumes:
    directory_path = os.path.dirname(self.volumes[0].fullPath())
    return os.path.join(directory_path, 'spm12_serial_job.m')

def execution( self, context ):
  serial = SerialLongitudinalRegistration()

  serial.setVolumes([diskitem.fullPath() for diskitem in self.volumes])
  serial.setTimes(self.times)
  if self.noise_estimate == "NaN":
    serial.setNoiseEstimateToNaN()
  elif self.noise_estimate in ["Scalar", "Matrix"]:
    serial.setNoiseEstimate(self.noise_estimate_value)
  else:
    raise ValueError("Unvalid noise_estimate")

  serial.setWarpingRegulariation(self.warping_regularisation)
  serial.setBiasRegularisation(self.bias_regularisation)
  if self.save_MPA:
    serial.saveMidPointAverage()
    if self.customs_outputs:
      serial.setOutputMidPointAverage(self.MPA.fullPath())
  else:
    serial.discardMidPointAverage()
  if self.save_jacobians:
    serial.saveJacobians()
    if self.customs_outputs:
      serial.setOutputJacobians([diskitem.fullPath() for diskitem in self.jacobians])
  else:
    serial.discardJacobians()
  if self.divergences:
    serial.saveDivergences()
    if self.customs_outputs:
      serial.setOutputDivergences([diskitem.fullPath() for diskitem in self.divergences])
  else:
    serial.discardDivergences()
  if self.save_deformation_fields:
    serial.saveDeformationFields()
    if self.customs_outputs:
      serial.setOutputVolumeDeformationField([diskitem.fullPath() for diskitem in self.deformation_fields])
  else:
    serial.discardDeformationFields()

  spm = validation()
  spm.addModuleToExecutionQueue(serial)
  spm.setSPMScriptPath(self.batch_location.fullPath())
  output = spm.run()
  context.log(name, html=output)
