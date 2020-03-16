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
from soma.spm.spm12.spatial.old_normalise import Write
from soma.spm.spm12.spatial.old_normalise.subject import SubjectToWrite
from soma.spm.spm12.spatial.old_normalise.writing_options import WritingOptions
from soma.spm.spm_launcher import SPM12, SPM12Standalone

import numpy

#------------------------------------------------------------------------------
configuration = Application().configuration
#------------------------------------------------------------------------------
def validation():
  try:
    spm = SPM12Standalone(configuration.SPM.spm8_standalone_command,
                          configuration.SPM.spm8_standalone_mcr_path,
                          configuration.SPM.spm8_standalone_path)
  except:
    spm = SPM12(configuration.SPM.spm8_path,
                configuration.matlab.executable,
                configuration.matlab.options)
  return spm
#------------------------------------------------------------------------------

userLevel = 1
name = 'spm12 - Old normalise: Write only - generic'

subject_section = "subject options"
writing_section = "writing options"

signature = Signature(
  "sn_mat", ReadDiskItem("Matlab SPM script", "Matlab file", section="SPM outputs"),
  "images_to_write", ListOf(ReadDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image']), section=subject_section),

  "preserve", Choice("Preserve Concentrations",
                     "Preserve Amount",
                     section=writing_section),
  "bounding_box", Matrix(length=2, width=3, section=writing_section),
  "voxel_size", ListOf(Float(),section=writing_section),
  "interpolation", Choice("Nearest neighbour",
                          "Trilinear",
                          "2nd Degree B-Spline",
                          "3rd Degree B-Spline",
                          "4th Degree B-Spline",
                          "5th Degree B-Spline",
                          "6th Degree B-Spline",
                          "7th Degree B-Spline",
                          section=writing_section),
  "wrappping", Choice(("No wrap",[False, False, False]),
                      ("Wrap X",[True, False, False]),
                      ("Wrap Y",[False, True, False]),
                      ("Wrap X & Y",[True, True, False]),
                      ("Wrap Z",[False, False, True]),
                      ("Wrap X & Z",[True, False, True]),
                      ("Wrap Y & Z",[False, True, True]),
                      ("Wrap X, Y & Z",[True, True, True]),
                      section=writing_section),

  "filename_prefix", String(section="outputs"),
  "images_written", ListOf(WriteDiskItem("4D Volume", ["gz compressed NIFTI-1 image", "NIFTI-1 image"]), section="outputs"),
  'batch_location', WriteDiskItem("Matlab SPM script", "Matlab script", section="default SPM outputs"),
)
def initialization(self):
  self.setOptional("images_written", "sn_mat")
  self.addLink(None, "filename_prefix", self.checkIfNotEmpty)

  self.addLink("batch_location", "sn_mat", self.updateBatchPath)

  #SPM default initialisation
  self.preserve = "Preserve Concentrations"
  self.bounding_box = [[-78, -112, -70],[78, 76, 85]]
  self.voxel_size = [2, 2, 2]
  self.interpolation = "Trilinear"
  self.wrappping = "No wrap"
  self.filename_prefix = 'w'

def checkIfNotEmpty(self, proc):
  if self.filename_prefix in [None, '']:
    self.filename_prefix = 'w'
  else:
    pass

def updateBatchPath(self, proc):
  if self.sn_mat is not None:
    directory_path = os.path.dirname(self.sn_mat.fullPath())
    return os.path.join(directory_path, 'spm8_normalise_EW_job.m')

def execution( self, context ):
  write = Write()

  subject = SubjectToWrite()
  subject.setParameterFile(self.sn_mat.fullPath())
  subject.setImageListToWrite([diskitem.fullPath() for diskitem in self.images_to_write])
  if self.images_written:
    if len(self.images_to_write) == len(self.images_written):
      subject.setImageListWritten([diskitem.fullPath() for diskitem in self.images_written])
    else:
      raise ValueError("images_to_write and images_written must have the same length")
  else:
    pass#SPM default outputs


  write.appendSubject(subject)

  writing_options = WritingOptions()
  if self.preserve == "Preserve Concentrations":
    writing_options.setPreserveToConcentrations()
  elif self.preserve == "Preserve Amount":
    writing_options.setPreserveToAmount()
  else:
    raise ValueError("Unvalid choice for preserve")

  writing_options.setBoundingBox(numpy.array(self.bounding_box))
  writing_options.setVoxelSize(self.voxel_size)

  if self.interpolation == "Nearest neighbour":
    writing_options.setInterpolationToNearestNeighbour()
  elif self.interpolation == "Trilinear":
    writing_options.setInterpolationToTrilinear()
  elif self.interpolation == "2nd Degree B-Spline":
    writing_options.setInterpolationTo2ndDegreeBSpline()
  elif self.interpolation == "3rd Degree B-Spline":
    writing_options.setInterpolationTo3rdDegreeBSpline()
  elif self.interpolation == "4th Degree B-Spline":
    writing_options.setInterpolationTo4thDegreeBSpline()
  elif self.interpolation == "5th Degree B-Spline":
    writing_options.setInterpolationTo5thDegreeBSpline()
  elif self.interpolation == "6th Degree B-Spline":
    writing_options.setInterpolationTo6thDegreeBSpline()
  elif self.interpolation == "7th Degree B-Spline":
    writing_options.setInterpolationTo7thDegreeBSpline()
  else:
    raise ValueError("Unvalid interpolation")

  writing_options.setWrapping(self.wrappping[0], self.wrappping[1], self.wrappping[2])
  writing_options.setFilenamePrefix(self.filename_prefix)

  write.replaceWrintingOptions(writing_options)

  spm = validation()
  spm.addModuleToExecutionQueue(write)
  spm.setSPMScriptPath(self.batch_location.fullPath())
  output = spm.run()
  context.log(name, html=output)
