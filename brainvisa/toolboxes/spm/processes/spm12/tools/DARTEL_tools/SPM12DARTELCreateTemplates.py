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
name = 'spm12 - Run DARTEL (create Templates)'

#------------------------------------------------------------------------------

signature = Signature(
    'images_1', ListOf( ReadDiskItem( "T1 MRI tissue probability map", ["gz compressed NIFTI-1 image", "NIFTI-1 image", "SPM image", "MINC image"] ) ),
    'images_2', ListOf( ReadDiskItem( "T1 MRI tissue probability map", ["gz compressed NIFTI-1 image", "NIFTI-1 image", "SPM image", "MINC image"] ) ),
    'output_flow_field', ListOf( WriteDiskItem( "HDW DARTEL flow field", ["gz compressed NIFTI-1 image", "NIFTI-1 image"] ) ),
    'output_template', ListOf( WriteDiskItem( "TPM HDW DARTEL created template", ["gz compressed NIFTI-1 image", "NIFTI-1 image"] ) ),
    'template_basename', String(),
    'regularisation_form', Choice('Linear Elastic Energy',
                                  'Membrane Energy',
                                  'Bending Energy'),

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

#------------------------------------------------------------------------------

def initialization(self):
    self.setOptional('images_2', 'output_flow_field', 'output_template')

    self.linkParameters('output_flow_field', ('images_1', 'template_basename'), self.updateFlowFields)
    self.linkParameters('output_template', ('images_1', 'template_basename'), self.updateDartelTemplate)

    self.addLink("batch_location", "output_template", self.updateBatchPath)

    self.template_basename = 'Template'
    self.regularisation_form = 'Linear Elastic Energy'

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

def updateFlowFields(self, proc, dummy):
  if self.images_1 and self.template_basename:
    output_diskitem_list = []
    for diskitem in self.images_1:
      d = diskitem.hierarchyAttributes()
      d['template'] = self.template_basename
      output_diskitem_list.append(WriteDiskItem( 'HDW DARTEL flow field', 'NIFTI-1 image' ).findValue(d))
    return output_diskitem_list

def updateDartelTemplate(self, proc, dummy):
  if self.images_1 and self.template_basename:
    output_diskitem_list = []
    diskitem = self.images_1[0]
    d = diskitem.hierarchyAttributes()
    d['template'] = self.template_basename
    for index in [1,2,3,4,5,6]:#TODO : 1->6 is the inner number...
      d['step'] = str(index)
      output_diskitem_list.append(WriteDiskItem( 'TPM HDW DARTEL created template', 'NIFTI-1 image' ).findValue(d))
    return output_diskitem_list

def updateBatchPath(self, proc):
  if self.output_template:
    directory_path = os.path.dirname(self.output_template[0].fullPath())
    return os.path.join(directory_path, 'spm12_DARTEL_create_template_job.m')
#------------------------------------------------------------------------------
def execution( self, context ):
  context.runProcess('SPM12DARTELCreateTemplates_generic',
                     images_1=self.images_1,
                     images_2=self.images_2,
                     output_flow_field=self.output_flow_field,
                     output_template=self.output_template,
                     template_basename=self.template_basename,
                     regularisation_form=self.regularisation_form,
                     inner_iteration_1=self.inner_iteration_1,
                     regularisation_parameters_1=self.regularisation_parameters_1,
                     time_step_1=self.time_step_1,
                     smoothing_parameter_1=self.smoothing_parameter_1,
                     inner_iteration_2=self.inner_iteration_2,
                     regularisation_parameters_2=self.regularisation_parameters_2,
                     time_step_2=self.time_step_2,
                     smoothing_parameter_2=self.smoothing_parameter_2,
                     inner_iteration_3=self.inner_iteration_3,
                     regularisation_parameters_3=self.regularisation_parameters_3,
                     time_step_3=self.time_step_3,
                     smoothing_parameter_3=self.smoothing_parameter_3,
                     inner_iteration_4=self.inner_iteration_4,
                     regularisation_parameters_4=self.regularisation_parameters_4,
                     time_step_4=self.time_step_4,
                     smoothing_parameter_4=self.smoothing_parameter_4,
                     inner_iteration_5=self.inner_iteration_5,
                     regularisation_parameters_5=self.regularisation_parameters_5,
                     time_step_5=self.time_step_5,
                     smoothing_parameter_5=self.smoothing_parameter_5,
                     inner_iteration_6=self.inner_iteration_6,
                     regularisation_parameters_6=self.regularisation_parameters_6,
                     time_step_6=self.time_step_6,
                     smoothing_parameter_6=self.smoothing_parameter_6,
                     LM_Regularisation=self.LM_Regularisation,
                     cycles=self.cycles,
                     iterations=self.iterations,
                     batch_location=self.batch_location)

