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
from soma.spm.spm12.tools.dartel_tools.run_dartel import RunDartel
from soma.spm.spm12.tools.dartel_tools.run_dartel.outer_iteration import OuterIteration
from soma.spm.spm12.tools.dartel_tools.run_dartel.optimisation_settings import OptimisationSettings
from soma.spm.spm12.tools.dartel_tools.run_dartel.settings import Settings
from soma.spm.spm_launcher import SPM12, SPM12Standalone
from soma.spm.spm_batch_maker_utils import copyNifti
from six.moves import range

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
name = 'spm12 - Run DARTEL (create Templates) - generic'

#------------------------------------------------------------------------------

signature = Signature(
    'images_1', ListOf( ReadDiskItem( '4D Volume', ["gz compressed NIFTI-1 image", 'NIFTI-1 image', 'SPM image', 'MINC image'] ) ),
    'images_2', ListOf( ReadDiskItem( '4D Volume', ["gz compressed NIFTI-1 image", 'NIFTI-1 image', 'SPM image', 'MINC image'] ) ),
    'output_flow_field', ListOf( WriteDiskItem( '4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"] ) ),
    'output_template', ListOf( WriteDiskItem( '4D Volume', ["gz compressed NIFTI-1 image", "NIFTI-1 image"] ) ),
    'template_basename', String(),
    'regularisation_form', Choice('Linear Elastic Energy',
                                  'Membrane Energy',
                                  'Bending Energy'),

    'outer_iterations', Integer(),

    # Outer Iteration 1
    'inner_iteration_1', Choice(1, 2, 3 ,4, 5 ,6 ,7 ,8, 9 ,10),
    'regularisation_parameters_1', ListOf(Float()),
    'time_step_1', Choice(1, 2, 4, 8, 16, 32, 64, 128, 256, 512),
    'smoothing_parameter_1', Choice("""None""",  0.5, 1, 2, 4, 8, 16, 32),

    # Outer Iteration 2
    'inner_iteration_2', Choice(1, 2, 3 ,4, 5 ,6 ,7 ,8, 9 ,10),
    'regularisation_parameters_2', ListOf(Float()),
    'time_step_2', Choice(1, 2, 4, 8, 16, 32, 64, 128, 256, 512),
    'smoothing_parameter_2', Choice("""None""",  0.5, 1, 2, 4, 8, 16, 32),

    # Outer Iteration 3
    'inner_iteration_3', Choice(1, 2, 3 ,4, 5 ,6 ,7 ,8, 9 ,10),
    'regularisation_parameters_3', ListOf(Float()),
    'time_step_3', Choice(1, 2, 4, 8, 16, 32, 64, 128, 256, 512),
    'smoothing_parameter_3', Choice("""None""",  0.5, 1, 2, 4, 8, 16, 32),

    # Outer Iteration 4
    'inner_iteration_4', Choice(1, 2, 3 ,4, 5 ,6 ,7 ,8, 9 ,10),
    'regularisation_parameters_4', ListOf(Float()),
    'time_step_4', Choice(1, 2, 4, 8, 16, 32, 64, 128, 256, 512),
    'smoothing_parameter_4', Choice("""None""",  0.5, 1, 2, 4, 8, 16, 32),

    # Outer Iteration 5
    'inner_iteration_5', Choice(1, 2, 3 ,4, 5 ,6 ,7 ,8, 9 ,10),
    'regularisation_parameters_5', ListOf(Float()),
    'time_step_5', Choice(1, 2, 4, 8, 16, 32, 64, 128, 256, 512),
    'smoothing_parameter_5', Choice("""None""",  0.5, 1, 2, 4, 8, 16, 32),

    # Outer Iteration 6
    'inner_iteration_6', Choice(1, 2, 3 ,4, 5 ,6 ,7 ,8, 9 ,10),
    'regularisation_parameters_6', ListOf(Float()),
    'time_step_6', Choice(1, 2, 4, 8, 16, 32, 64, 128, 256, 512),
    'smoothing_parameter_6', Choice("""None""",  0.5, 1, 2, 4, 8, 16, 32),

    # Optimisation settings
    'LM_Regularisation', Float(),
    'cycles', Choice(1, 2, 3, 4, 5, 6, 7, 8),
    'iterations', Choice(1, 2, 3, 4, 5, 6, 7, 8),

    'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script', section='default SPM outputs'),
 )

INNER_ITERATION_PARAM_PREFIXES = (
    'inner_iteration_', 'regularisation_parameters_',
    'time_step_', 'smoothing_parameter_',
)

#------------------------------------------------------------------------------

def initialization(self):
    self.setOptional('images_2', 'output_flow_field', 'output_template')

    self.addLink("batch_location", "output_template", self.updateBatchPath)
    self.addLink(None, "outer_iterations", self.updateSignature)

    self.template_basename = 'Template'
    self.regularisation_form = 'Linear Elastic Energy'

    self.outer_iterations = 6

    self.inner_iteration_1 = 3
    self.regularisation_parameters_1 = [4, 2, 1e-06]
    self.time_step_1 = 1
    self.smoothing_parameter_1 = 16

    self.inner_iteration_2 = 3
    self.regularisation_parameters_2 = [2, 1, 1e-06]
    self.time_step_2 = 1
    self.smoothing_parameter_2 = 8

    self.inner_iteration_3 = 3
    self.regularisation_parameters_3 = [1, 0.5, 1e-06]
    self.time_step_3 = 2
    self.smoothing_parameter_3 = 4

    self.inner_iteration_4 = 3
    self.regularisation_parameters_4 = [0.5, 0.25, 1e-06]
    self.time_step_4 = 4
    self.smoothing_parameter_4 = 2

    self.inner_iteration_5 = 3
    self.regularisation_parameters_5 = [0.25, 0.125, 1e-06]
    self.time_step_5 = 16
    self.smoothing_parameter_5 = 1

    self.inner_iteration_6 = 3
    self.regularisation_parameters_6 = [0.25, 0.125, 1e-06]
    self.time_step_6 = 64
    self.smoothing_parameter_6 = 0.5

    self.LM_Regularisation = 0.01
    self.cycles = 3
    self.iterations = 3

def updateBatchPath(self, proc):
  if self.output_template:
    directory_path = os.path.dirname(self.output_template[0].fullPath())
    return os.path.join(directory_path, 'spm12_DARTEL_create_template_job.m')


def updateSignature(self, proc):
  signature = self.signature

  for i in range(2, self.outer_iterations + 1):
    for prefix in INNER_ITERATION_PARAM_PREFIXES:
      signature[prefix + str(i)] = signature[prefix + '1']

  # delete extra parameters (if self.outer_iterations was decreased)
  i = max(self.outer_iterations + 1, 2)
  while 'inner_iteration_' + str(i) in signature:
    for prefix in INNER_ITERATION_PARAM_PREFIXES:
      del signature[prefix + str(i)]
    i += 1

  self.changeSignature(signature)

#------------------------------------------------------------------------------
def execution( self, context ):
  if self.images_2:
    if len(self.images_1) != len(self.images_2):
      context.error("the length of images_1 and images_2 must be the same")
      raise ValueError
    else:
      pass
  else:
    pass
#==============================================================================
# convert volumes (to keep spm internal transorm in qform or if 5D volume)
#==============================================================================
  images_1_diskitem_list = convertDiskitemList(context, self.images_1)
  if self.images_2:
    images_2_diskitem_list = convertDiskitemList(context, self.images_2)
#==============================================================================
  run_dartel = RunDartel()
  run_dartel.setFirstImageList([diskitem.fullPath() for diskitem in images_1_diskitem_list])
  if self.images_2:
    run_dartel.appendImageList([diskitem.fullPath() for diskitem in images_2_diskitem_list])

  if self.output_flow_field:
    run_dartel.setOutputFlowFieldPathList([diskitem.fullPath() for diskitem in self.output_flow_field])

  if self.output_template:
    run_dartel.setOutputTemplatePathList([diskitem.fullPath() for diskitem in self.output_template])

  settings = Settings()
  settings.clearOuterIterationContainer()
  settings.setTemplateBasename(self.template_basename)
  if self.regularisation_form == 'Linear Elastic Energy':
    settings.setRegularisationFormToLinearElasticEnergy()
  elif self.regularisation_form == 'Membrane Energy':
    settings.setRegularisationFormToMembraneEnergy()
  elif self.regularisation_form == 'Bending Energy':
    settings.setRegularisationFormToBendingEnergy()
  else:
    raise ValueError("Invalid choice for regularisation_form")

  for i in range(1, self.outer_iterations + 1):
    i_str = str(i)
    outer_iteration = OuterIteration()
    outer_iteration.setInnerIterationsNumber(getattr(self, 'inner_iteration_' + i_str))
    outer_iteration.setRegParams(getattr(self, 'regularisation_parameters_' + i_str))
    outer_iteration.setTimeSteps(getattr(self, 'time_step_' + i_str))
    outer_iteration.setSmoothingParameter(getattr(self, 'smoothing_parameter_' + i_str))
    settings.appendOuterIteration(outer_iteration)

  optimisation_settings = OptimisationSettings()
  optimisation_settings.setLMRegularisation(self.LM_Regularisation)
  optimisation_settings.setCycles(self.cycles)
  optimisation_settings.setIterations(self.iterations)

  settings.setOptimisationSettings(optimisation_settings)

  run_dartel.setSettings(settings)

  spm = validation()
  spm.addModuleToExecutionQueue(run_dartel)
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

