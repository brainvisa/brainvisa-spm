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
from soma.spm.spm12.util.image_calculator import ImageCalculator
from soma.spm.spm12.util.image_calculator.additional_variable import AdditionalVariable
from soma.spm.spm12.util.image_calculator.options import Options
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
name = 'spm12 - Image calculator - generic'

signature = Signature(
  'input_images', ListOf(ReadDiskItem('4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'])),
  'output_image', WriteDiskItem('4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"]),
  'expression', String(),
  'data_matrix', Boolean(),
  'masking', Choice('No implicit zero mask', 'Implicit zero mask', 'NaNs should be zeroed'),
  "interpolation", Choice("Nearest neighbour",
                          "Trilinear",
                          "2nd Degree B-Spline",
                          "3rd Degree B-Spline",
                          "4th Degree B-Spline",
                          "5th Degree B-Spline",
                          "6th Degree B-Spline",
                          "7th Degree B-Spline"),
  'data_type', Choice("UINT8   - unsigned char",
                      "INT16   - signed short",
                      "INT32   - signed int",
                      "FLOAT32 - single prec. float",
                      "FLOAT64 - double prec. float"),
  #Batch
  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script', section='default SPM outputs' )
)

def initialization(self):
  self.addLink("batch_location", "output_image", self.updateBatchPath)

  self.data_matrix = False
  self.masking = "No implicit zero mask"
  self.interpolation = "Trilinear"
  self.data_type = "INT16   - signed short"

def updateBatchPath(self, proc):
  if self.output_image is not None:
    ouput_directory = os.path.dirname(self.output_image.fullPath())
    return os.path.join(ouput_directory, 'spm12_imcalc_job.m')

def execution(self, context):
  imcalc = ImageCalculator()
  imcalc.setInputImagePathList([diskitem.fullPath() for diskitem in self.input_images])
  imcalc.setOutputImagePath(self.output_image.fullPath())
  imcalc.setExpression(self.expression)

  #=============================================================================
  # var_1 = AdditionalVariable()
  # var_1.setName("first_var")
  # var_1.setValue(numpy.array(...))
  # imcalc.appendAdditionalVariable(var_1)
  #=============================================================================

  options = Options()
  if self.data_matrix:
    options.setDataMatrix()
  else:
    options.unsetDataMatrix()

  if self.masking == "No implicit zero mask":
    options.setMaskingTypeToNoImplicitZero()
  elif self.masking == "Implicit zero mask":
    options.setMaskingTypeToImplicitZero()
  elif self.masking == "NaNs should be zeroed":
    options.setMaskingTypeToNaNShouldBeZeroed()
  else:
    raise ValueError("Unvalid choice for masking")

  if self.interpolation == "Nearest neighbour":
    options.setInterpolationToNearestNeighbour()
  elif self.interpolation == "Trilinear":
    options.setInterpolationToTrilinear()
  elif self.interpolation == "2nd Degree B-Spline":
    options.setInterpolationTo2ndDegreeBSpline()
  elif self.interpolation == "3rd Degree B-Spline":
    options.setInterpolationTo3rdDegreeBSpline()
  elif self.interpolation == "4th Degree B-Spline":
    options.setInterpolationTo4thDegreeBSpline()
  elif self.interpolation == "5th Degree B-Spline":
    options.setInterpolationTo5thDegreeBSpline()
  elif self.interpolation == "6th Degree B-Spline":
    options.setInterpolationTo6thDegreeBSpline()
  elif self.interpolation == "7th Degree B-Spline":
    options.setInterpolationTo7thDegreeBSpline()
  else:
    raise ValueError("Unvalid choice for interpolation")

  if self.data_type == "UINT8   - unsigned char":
    options.setDataTypeToUint8()
  elif self.data_type == "INT16   - signed short":
    options.setDataTypeToInt16()
  elif self.data_type == "INT32   - signed int":
    options.setDataTypeToInt32()
  elif self.data_type == "FLOAT32 - single prec. float":
    options.setDataTypeToFloat32()
  elif self.data_type == "FLOAT64 - double prec. float":
    options.setDataTypeToFloat64()
  else:
    raise ValueError("Unvalid choice for data_type")

  imcalc.replaceOptions(options)

  spm = validation()
  spm.addModuleToExecutionQueue(imcalc)
  spm.setSPMScriptPath(self.batch_location.fullPath())
  output = spm.run()
  context.log(name, html=output)
