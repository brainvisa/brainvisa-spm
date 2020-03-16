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
from soma.spm.spm8.spatial.smooth import Smooth
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
name = 'spm8 - Smooth - generic'

signature = Signature(
  "images", ListOf(ReadDiskItem("4D Volume", ['NIFTI-1 image', 'SPM image', 'MINC image'])),
  "fwhm", ListOf(Float()),
  'data_type', Choice("SAME",
                      "UINT8   - unsigned char",
                      "INT16   - signed short",
                      "INT32   - signed int",
                      "FLOAT32 - single prec. float",
                      "FLOAT64 - double prec. float"),
  "implicit_masking", Boolean(),
  "custom_outputs", Boolean(),
  "filename_prefix", String(),
  "images_smoothed", ListOf(WriteDiskItem("4D Volume", ["gz compressed NIFTI-1 image", "NIFTI-1 image"])),
  #Batch
  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script', section='default SPM outputs' )
)
def initialization(self):
  self.setOptional("images_smoothed")

  self.addLink(None, "custom_outputs", self.updateSignatureAboutCustomOutputs)
  self.addLink(None, "filename_prefix", self.checkIfNotEmpty)

  self.addLink("batch_location", "images", self.updateBatchPath)

  #SPM default initialisation
  self.fwhm = [8, 8, 8]
  self.data_type = "SAME"
  self.implicit_masking = False
  self.filename_prefix = 's'

  self.custom_outputs = False

def updateSignatureAboutCustomOutputs(self, proc):
  if self.custom_outputs:
    self.setEnable("images_smoothed")
    self.setDisable("filename_prefix")
  else:
    self.setDisable("images_smoothed")
    self.setEnable("filename_prefix")
  self.signatureChangeNotifier.notify( self )

def checkIfNotEmpty(self, proc):
  if self.filename_prefix in [None, '']:
    self.filename_prefix = 's'
  else:
    pass

def updateBatchPath(self, proc):
  if self.images:
    directory_path = os.path.dirname(self.images[0].fullPath())
    return os.path.join(directory_path, 'spm8_smooth_job.m')

def execution( self, context ):
  smooth = Smooth()
  smooth.setInputImagePathList([diskitem.fullPath() for diskitem in self.images])
  smooth.setFilenamePrefix(self.filename_prefix)

  if self.custom_outputs:
    if len(self.images) == len(self.images_smoothed):
      smooth.setOutputImagePathList([diskitem.fullPath() for diskitem in self.images_smoothed])
    else:
      raise ValueError("images has not the same length than images_smoothed")
  else:
    pass#prefix used

  if len(self.fwhm) == 3:
    smooth.setFWHM(self.fwhm[0], self.fwhm[1], self.fwhm[2])
  else:
    raise ValueError("Three  values  should  be  entered,  denoting the FWHM in the x, y and z  directions")

  if self.data_type == "SAME":
    smooth.setDataTypeToSame()
  elif self.data_type == "UINT8   - unsigned char":
    smooth.setDataTypeToUint8()
  elif self.data_type == "INT16   - signed short":
    smooth.setDataTypeToInt16()
  elif self.data_type == "INT32   - signed int":
    smooth.setDataTypeToInt32()
  elif self.data_type == "FLOAT32 - single prec. float":
    smooth.setDataTypeToFloat32()
  elif self.data_type == "FLOAT64 - double prec. float":
    smooth.setDataTypeToFloat64()
  else:
    raise ValueError("Unvalid choice for data_type")

  if self.implicit_masking:
    smooth.setImplicitMasking()
  else:
    smooth.unsetImplicitMasking()

  spm = validation()
  spm.addModuleToExecutionQueue(smooth)
  spm.setSPMScriptPath(self.batch_location.fullPath())
  output = spm.run()
  context.log(name, html=output)
