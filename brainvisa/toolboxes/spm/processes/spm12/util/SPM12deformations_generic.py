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
import tempfile
from soma.spm.spm12.util.deformations import Composition, Deformations
# from soma.spm.spm12.util.deformations.composition import MatFileImported
# from soma.spm.spm12.util.deformations.composition import DartelFlow
from soma.spm.spm12.util.deformations.composition import DeformationField
# from soma.spm.spm12.util.deformations.composition import IdentityFromImage
# from soma.spm.spm12.util.deformations.composition import Identity
from soma.spm.spm12.util.deformations.composition import Inverse
from soma.spm.spm12.util.deformations.output import PullBack, PushFoward
from soma.spm.spm_batch_maker_utils import copyNifti
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
name = 'spm12 - Deformations : apply deformation field- generic'
#TODO : Add all available compositions but BV interface is not very efficient to do this
signature = Signature(
  'input_images', ListOf(ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'])),#TODO : modify because 4D is unvailable from SPM
  'deformation_field', ReadDiskItem('4D Volume', ["gz compressed NIFTI-1 image", 'NIFTI-1 image', 'SPM image', 'MINC image']),
  'apply_inverse', Boolean(),
  'reference_volume', ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image']),
  'interpolation', Choice("Nearest neighbour",
                          "Trilinear",
                          "2nd Degree B-Spline",
                          "3rd Degree B-Spline",
                          "4th Degree B-Spline",
                          "5th Degree B-Spline",
                          "6th Degree B-Spline",
                          "7th Degree B-Spline"),
  'masking', Boolean(),
  'gaussian_fwhm', ListOf(Float()),
  'output_destination', Choice('Current directory',
                               'Source directories',
                               'Output directory'),
  'ouput_directory', WriteDiskItem('Directory', 'Directory'),
  'custom_outputs', Boolean(),
  'images_deformed', ListOf(WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"])),
  #Batch
  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script', section='default SPM outputs' )
)

def initialization(self):
  self.addLink(None, 'apply_inverse', self.updateSignatureAboutInverse)
  self.addLink(None, 'custom_outputs', self.updateSignatureAboutOutputs)
  self.addLink(None, 'output_destination', self.updateSignatureAboutOutputDestination)

  self.addLink("batch_location", "deformation_field", self.updateBatchPath)

  self.apply_inverse = False
  self.interpolation = "4th Degree B-Spline"
  self.gaussian_fwhm = [0, 0, 0]
  self.custom_outputs = False


def updateSignatureAboutInverse(self, proc):
  if self.apply_inverse:
    self.setEnable('reference_volume')
  else:
    self.setDisable('reference_volume')
  self.changeSignature(self.signature)

def updateSignatureAboutOutputs(self, proc):
  if self.custom_outputs:
    self.setEnable('images_deformed')
  else:
    self.setDisable('images_deformed')
  self.changeSignature(self.signature)

def updateSignatureAboutOutputDestination(self, proc):
  if self.output_destination == 'Output directory':
    self.setEnable('ouput_directory')
  else:
    self.setDisable('ouput_directory')
  self.changeSignature(self.signature)

def updateBatchPath(self, proc):
  if self.deformation_field is not None:
    ouput_directory = os.path.dirname(self.deformation_field.fullPath())
    return os.path.join(ouput_directory, 'spm12_deformations_job.m')

def execution(self, context):
  if str(self.deformation_field.format) == "gz compressed NIFTI-1 image":
    deformation_fullpath = tempfile.NamedTemporaryFile(prefix="y_", suffix=".nii").name
    copyNifti(self.deformation_field.fullPath(), deformation_fullpath)
  else:
    deformation_fullpath = self.deformation_field.fullPath()

  deformations = Deformations()

  deformation_field = DeformationField()
  deformation_field.setDeformationFieldPath(deformation_fullpath)

  if self.apply_inverse:
    comp = Composition()
    comp.append(deformation_field)
    inverse = Inverse()
    inverse.setDeformationComposition(comp)
    inverse.setImageToBaseInverseOn(self.reference_volume.fullPath())
    deformations.appendDeformation(inverse)
  else:
    deformations.appendDeformation(deformation_field)


  pull_back = PullBack()
  pull_back.setVolumeListToApply([diskitem.fullPath() for diskitem in self.input_images])

  if self.custom_outputs:
    pull_back.setOuputPathList([diskitem.fullPath() for diskitem in self.images_deformed])

  if self.output_destination == 'Current directory':
#     deformations.setOuputDestinationToCurrentDirectory()#SPM current directory == batch directory
    pull_back.setOutputDestinationToOutputDirectory(os.path.dirname(self.batch_location.fullPath()))
  elif self.output_destination == 'Source directories':
    pull_back.setOuputDestinationToSourceDirectories()
  elif self.output_destination == 'Output directory':
    if not os.path.exists(self.ouput_directory.fullPath()):
      os.makedirs(self.ouput_directory.fullPath())
    else:
      pass#directory already exists
    pull_back.setOutputDestinationToOutputDirectory(self.ouput_directory.fullPath())
  else:
    raise ValueError("Unvalid output_destination")

  if self.interpolation == "Nearest neighbour":
    pull_back.setInterpolationToNearestNeighbour()
  elif self.interpolation == "Trilinear":
    pull_back.setInterpolationToTrilinear()
  elif self.interpolation == "2nd Degree B-Spline":
    pull_back.setInterpolationTo2ndDegreeBSpline()
  elif self.interpolation == "3rd Degree B-Spline":
    pull_back.setInterpolationTo3rdDegreeBSpline()
  elif self.interpolation == "4th Degree B-Spline":
    pull_back.setInterpolationTo4thDegreeBSpline()
  elif self.interpolation == "5th Degree B-Spline":
    pull_back.setInterpolationTo5thDegreeBSpline()
  elif self.interpolation == "6th Degree B-Spline":
    pull_back.setInterpolationTo6thDegreeBSpline()
  elif self.interpolation == "7th Degree B-Spline":
    pull_back.setInterpolationTo7thDegreeBSpline()
  else:
    raise ValueError("Unvalid interpolation")

  if self.masking:
    pull_back.setMasking()
  else:
    pull_back.unsetMasking()

  if len(self.gaussian_fwhm) == 3:
    pull_back.setFWHM(self.gaussian_fwhm[0],
                      self.gaussian_fwhm[1],
                      self.gaussian_fwhm[2])
  else:
    context.error("gaussian_fwhm requires 3 value")

  deformations.appendOutput(pull_back)

  spm = validation()
  spm.addModuleToExecutionQueue(deformations)
  spm.setSPMScriptPath(self.batch_location.fullPath())
  output = spm.run()
  context.log(name, html=output)
