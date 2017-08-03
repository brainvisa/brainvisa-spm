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
from soma.spm.spm8.tools.dartel_tools.create_inverse_warped import CreateInverseWarped
from soma.spm.spm_launcher import SPM8, SPM8Standalone
from soma.spm.spm_batch_maker_utils import copyNifti

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
name = "spm8 - create inverse warped - generic"

#------------------------------------------------------------------------------

signature = Signature(
  "flow_fields", ListOf(ReadDiskItem( "4D Volume", ["gz compressed NIFTI-1 image", "NIFTI-1 image", "SPM image", "MINC image"])),
  "images", ListOf(ReadDiskItem( "4D Volume", ["gz compressed NIFTI-1 image", "NIFTI-1 image", "SPM image", "MINC image"])),
  "images_warped", ListOf(WriteDiskItem( "4D Volume", ["gz compressed NIFTI-1 image", "NIFTI-1 image"])),
  "time_steps", Choice(1, 2, 4, 8, 16, 32, 64, 128, 256, 512),
  "interpolation", Choice("Nearest neighbour",
                          "Trilinear",
                          "2nd Degree B-Spline",
                          "3rd Degree B-Spline",
                          "4th Degree B-Spline",
                          "5th Degree B-Spline",
                          "6th Degree B-Spline",
                          "7th Degree B-Spline"),

  "batch_location", WriteDiskItem("Matlab SPM script", "Matlab script", section="default SPM outputs"),
)
#------------------------------------------------------------------------------

def initialization(self):
    self.setOptional("images_warped")

    self.addLink("batch_location", "images_warped", self.updateBatchPath)

    #SPM8 default parameters
    self.time_steps = 64
    self.interpolation = "Trilinear"

def updateBatchPath(self, proc):
  if self.images_warped:
    return os.path.join(self.images_warped[0].fullPath(), 'spm8_DARTEL_created_inverse_warped_job.m')

def execution( self, context ):
#==============================================================================
# convert volumes (to keep spm internal transorm in qform or if 5D volume)
#==============================================================================
  flow_fields_diskitem_list = convertDiskitemList(context, self.flow_fields)
  images_diskitem_list = convertDiskitemList(context, self.images)
#==============================================================================
  create_inverse_warped = CreateInverseWarped()
  create_inverse_warped.setFlowFieldPathList([diskitem.fullPath() for diskitem in flow_fields_diskitem_list])
  create_inverse_warped.setImagePathList([diskitem.fullPath() for diskitem in images_diskitem_list])

  if self.images_warped:
    output_warped_list = [diskitem.fullPath() for diskitem in self.images_warped]
    create_inverse_warped.setOutputWarpedPathList(output_warped_list)

  create_inverse_warped.setTimeSteps(self.time_steps)

  if self.interpolation == "Nearest neighbour":
    create_inverse_warped.setInterpolationToNearestNeighbour()
  elif self.interpolation == "Trilinear":
    create_inverse_warped.setInterpolationToTrilinear()
  elif self.interpolation == "2nd Degree B-Spline":
    create_inverse_warped.setInterpolationTo2ndDegreeBSpline()
  elif self.interpolation == "3rd Degree B-Spline":
    create_inverse_warped.setInterpolationTo3rdDegreeBSpline()
  elif self.interpolation == "4th Degree B-Spline":
    create_inverse_warped.setInterpolationTo4thDegreeBSpline()
  elif self.interpolation == "5th Degree B-Spline":
    create_inverse_warped.setInterpolationTo5thDegreeBSpline()
  elif self.interpolation == "6th Degree B-Spline":
    create_inverse_warped.setInterpolationTo6thDegreeBSpline()
  elif self.interpolation == "7th Degree B-Spline":
    create_inverse_warped.setInterpolationTo7thDegreeBSpline()
  else:
    raise ValueError("Unvalid interpolation")

  spm = validation()
  spm.addModuleToExecutionQueue(create_inverse_warped)
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