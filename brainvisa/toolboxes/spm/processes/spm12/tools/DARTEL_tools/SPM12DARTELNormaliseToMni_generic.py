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
from soma.spm.spm12.tools.dartel_tools.normalise_to_mni import NormaliseToMNI
from soma.spm.spm_launcher import SPM12, SPM12Standalone
from soma.spm.spm12.tools.dartel_tools.normalise_to_mni.many_subjects import ManySubjects
import numpy
from soma.spm.spm_batch_maker_utils import copyNifti

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
name = 'spm12 - DARTEL - Normalise to mni - generic'

#------------------------------------------------------------------------------

signature = Signature(
  'final_space', Choice("MNI", "DARTEL"),
  'final_template', ReadDiskItem("4D Volume", ["gz compressed NIFTI-1 image", "NIFTI-1 image", "SPM image", "MINC image"]),
  'flow_fields', ListOf(ReadDiskItem("4D Volume", ["gz compressed NIFTI-1 image", "NIFTI-1 image", "SPM image", "MINC image"])),
  'images_0', ListOf(ReadDiskItem("4D Volume", ["gz compressed NIFTI-1 image", "NIFTI-1 image", "SPM image", "MINC image"])),
  'images_0_warped', ListOf(WriteDiskItem("4D Volume", ["gz compressed NIFTI-1 image", "NIFTI-1 image"])),

  "preserve", Choice("Preserve Concentrations",
                     "Preserve Amount"),
  "bounding_box",Choice("default : NaN", "custom"),
  "bounding_box_matrix", Matrix(length=2, width=3),
  "voxel_size",Choice("default : NaN", "custom"),
  "voxel_size_vector", ListOf(Float()),
  "fwhm", ListOf(Float()),

  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script', section='default SPM outputs'),
 )

#------------------------------------------------------------------------------

def initialization(self):
  self.setOptional('final_template', 'images_0_warped')

  self.addLink(None, "final_space", self.updateFinalTemplate)
  self.addLink(None, "bounding_box", self.updateSignatureAboutBoundingBox)
  self.addLink(None, "voxel_size", self.updateSignatureAboutVoxelSize)
  self.addLink("batch_location", "final_template", self.updateBatchPath)

  self.fwhm = [8, 8, 8]

def updateFinalTemplate(self, final_space, names, parameterized):
  if final_space == "MNI":
    self.setEnable("final_template")
  else:
    self.setDisable("final_template")
  self.changeSignature(self.signature)

def updateSignatureAboutBoundingBox(self, bounding_box, names, parameterized):
  if bounding_box == "default : NaN":
    self.setDisable("bounding_box_matrix")
  else:
    self.setEnable("bounding_box_matrix")
  self.changeSignature(self.signature)

def updateSignatureAboutVoxelSize(self, voxel_size, names, parameterized):
  if voxel_size == "default : NaN":
    self.setDisable("voxel_size_vector")
  else:
    self.setEnable("voxel_size_vector")
  self.changeSignature(self.signature)

def updateBatchPath(self, proc):
  if self.final_template is not None:
    final_template_dir = os.path.dirname(self.final_template.fullPath())
    return os.path.join(final_template_dir, 'spm12_DARTEL_normalise_to_mni_job.m')

#------------------------------------------------------------------------------
def execution( self, context ):
#==============================================================================
# convert volumes (to keep spm internal transorm in qform or if 5D volume)
#==============================================================================
  flow_fields_diskitem_list = convertDiskitemList(context, self.flow_fields)
  images_0_diskitem_list = convertDiskitemList(context, self.images_0)
  final_template = convertDiskitem(context, self.final_template)
#==============================================================================

  if self.bounding_box == "default : NaN":
    bounding_box = [["NaN", "NaN", "NaN"],["NaN", "NaN", "NaN"]]
  else:
    bounding_box = self.bounding_box_matrix

  if self.voxel_size == "default : NaN":
    voxel_size = ["NaN", "NaN", "NaN"]
  else:
    voxel_size = self.voxel_size_vector


  normalise = NormaliseToMNI()

  if self.final_space == "MNI":
    normalise.setFinalTemplatePath(final_template.fullPath())

  many_subjects = ManySubjects()
  many_subjects.setFlowFieldPathList([image.fullPath() for image in flow_fields_diskitem_list])
  many_subjects.appendImagePathList([image.fullPath() for image in images_0_diskitem_list])
  if self.images_0_warped:
    many_subjects.appendOutputImagePathList([image_warped.fullPath() for image_warped in self.images_0_warped])

  normalise.setAccordingToManySubjects(many_subjects)

  if self.preserve == "Preserve Concentrations":
    normalise.setPreserveToConcentrations()
  elif self.preserve == "Preserve Amount":
    normalise.setPreserveToAmount()
  else:
    raise ValueError("Unvalid preserve")

  normalise.setBoundingBox(numpy.array(bounding_box))
  normalise.setVoxelSize(voxel_size)

  if len(self.fwhm) == 3:
    normalise.setFWHM(self.fwhm[0], self.fwhm[1], self.fwhm[2])
  else:
    raise ValueError("Three  values  should  be  entered,  denoting the FWHM in the x, y and z  directions")

  spm = validation()
  spm.addModuleToExecutionQueue(normalise)
  spm.setSPMScriptPath(self.batch_location.fullPath())
  output = spm.run()
  context.log(name, html=output)
#==============================================================================
#
#==============================================================================
def convertDiskitemList(context, diskitem_list):
    new_diskitem_list = list()
    for diskitem in diskitem_list:
        new_diskitem_list.append(convertDiskitem(context, diskitem))
    return new_diskitem_list

def convertDiskitem(context, diskitem):
    """convert to .nii"""
    if str(diskitem.format) != "NIFTI-1 image":
        diskitem_tmp = context.temporary("NIFTI-1 image")
        copyNifti(diskitem.fullPath(), diskitem_tmp.fullPath())
        return diskitem_tmp
    else:
        return diskitem