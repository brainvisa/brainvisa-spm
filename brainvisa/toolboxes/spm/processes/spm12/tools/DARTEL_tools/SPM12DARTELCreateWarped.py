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
#------------------------------------------------------------------------------

userLevel = 0
name = "spm12 - create warped"

#------------------------------------------------------------------------------

signature = Signature(
  "flow_fields", ListOf(ReadDiskItem( "HDW DARTEL flow field", ["gz compressed NIFTI-1 image", "NIFTI-1 image", "SPM image", "MINC image"])),
  "DARTEL_directory", ReadDiskItem( "DARTEL analysis directory", "Directory"),
  "images_1", ListOf(ReadDiskItem( "T1 MRI tissue probability map", ["gz compressed NIFTI-1 image", "NIFTI-1 image", "SPM image", "MINC image"])),
  "images_2", ListOf(ReadDiskItem( "T1 MRI tissue probability map", ["gz compressed NIFTI-1 image", "NIFTI-1 image", "SPM image", "MINC image"])),
  "images_1_warped", ListOf(WriteDiskItem( "T1 MRI tissue probability map", ["gz compressed NIFTI-1 image", "NIFTI-1 image"])),
  "images_2_warped", ListOf(WriteDiskItem( "T1 MRI tissue probability map", ["gz compressed NIFTI-1 image", "NIFTI-1 image"])),
  "modulation", Boolean(),#TODO : hierarchy about modulation !!!!!
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
    self.setOptional("images_2",
                     "images_1_warped",
                     "images_2_warped")

    self.linkParameters("DARTEL_directory", "flow_fields")
    self.linkParameters("images_1", "flow_fields")
    self.linkParameters("images_2", "flow_fields")
    self.linkParameters("images_1_warped", "flow_fields")
    self.linkParameters("images_2_warped", "flow_fields")
    self.linkParameters("DARTEL_directory", "flow_fields", self.updateDARTELDirectory)

    self.addLink("batch_location", "DARTEL_directory", self.updateBatchPath)

    #SPM8 default parameters
    self.modulation = False
    self.time_steps = 64
    self.interpolation = "Trilinear"

def updateDARTELDirectory(self, proc, dummy):
  if self.flow_fields:
    d =self.flow_fields[0].hierarchyAttributes()
    return self.signature["DARTEL_directory"].findValue(d)

def updateBatchPath(self, proc):
  if self.DARTEL_directory is not None:
    return os.path.join(self.DARTEL_directory.fullPath(), 'spm12_DARTEL_created_warped_job.m')

def execution( self, context ):
  context.runProcess('SPM12DARTELCreateWarped_generic',
                     flow_fields=self.flow_fields,
                     images_1=self.images_1,
                     images_2=self.images_2,
                     images_1_warped=self.images_1_warped,
                     images_2_warped=self.images_2_warped,
                     modulation=self.modulation,
                     time_steps=self.time_steps,
                     interpolation=self.interpolation,
                     batch_location=self.batch_location)


