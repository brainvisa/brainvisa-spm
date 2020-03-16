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
from soma.spm import csv_converter
from soma.spm.spm8.stats.factorial_design import TwoSampleTTest
from soma.spm.spm8.stats.factorial_design.covariate import Covariate
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
name = 'spm8 - Two sample T-test - generic'

signature = Signature(
  #design
  'images_are_parametric', Boolean(),
  'group_1_images', ListOf( ReadDiskItem( '4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'] ) ),
  'group_2_images', ListOf( ReadDiskItem( '4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'] ) ),
  'independence',Boolean(),
  'variance', Choice('Unequal', 'Equal'),
  'grand_mean_scaling',Boolean(),
  'ANCOVA',Boolean(),
  #Covariates
  'covariate_table', ReadDiskItem('Covariate table for SPM', 'CSV file'),
  'covariate_list', ListOf(Choice()),
  #Masking
  'threshold_masking', Choice( "Neither", 'Absolute', 'Relative' ),
  'threshold_value', Float(),
  'implicit_mask', Boolean(),
  'explicit_mask', ReadDiskItem( '4D Volume',  ['NIFTI-1 image', 'SPM image', 'MINC image'] ),
  #Global calculation
  'global_calculation', Choice( 'Omit', 'User', 'Mean' ),
  'user_global_values', ListOf( Float() ),
  #Global normalisation
  'overall_grand_mean_scaling', Boolean(),
  'grand_mean_scaled_value', ListOf( Float() ),
  'normalisation', Choice("Neither", 'Proportional', 'ANCOVA'),
  'spm_workspace_directory', WriteDiskItem('Voxel by voxel comparison SPM workspace directory', 'Directory'),
  'two_sample_T_test_mat_file', WriteDiskItem( 'Matlab SPM file', 'Matlab file' ),
  #job_batch_file
  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script' ),
)

def initialization( self ):
  self.addLink(None, 'images_are_parametric', self.updateSignatureAboutParametricImages)
  self.addLink(None, 'covariate_table', self.updateCovariate)
  self.addLink( None, 'threshold_masking', self.updateThresholdMaskingFields)
  self.addLink( 'threshold_value', 'threshold_masking', self.updateThresholdMaskingValue)

  self.addLink( None, 'global_calculation', self.updateGlobalCalculationFields)

  self.addLink( None, 'overall_grand_mean_scaling', self.updateOverallGrandMeanScalingFields)

  self.addLink("batch_location", "spm_workspace_directory", self.updateBatchPath)

  self.setOptional('covariate_table', 'covariate_list', 'explicit_mask')

  self.signature['two_sample_T_test_mat_file'].userLevel = 1
  self.signature[ 'threshold_value' ].userLevel = 3
  self.signature[ 'threshold_value' ].mandatory = False
  self.signature[ 'user_global_values' ].userLevel = 3
  self.signature[ 'user_global_values' ].mandatory = False
  self.signature[ 'grand_mean_scaled_value' ].userLevel = 3
  self.signature[ 'grand_mean_scaled_value' ].mandatory = False

  self.grand_mean_scaling = False
  self.ANCOVA = False
  self.overall_grand_mean_scaling = False
  self.grand_mean_scaled_value = [50]

def updateSignatureAboutParametricImages(self, proc):
  if self.images_are_parametric:
    self.overall_grand_mean_scaling = False
    self.normalisation = "Neither"
  else:
    self.overall_grand_mean_scaling = True
    self.normalisation = 'Proportional'

def updateCovariate(self, proc):
  if self.covariate_table is not None:
    covariate_dict, row_keys_list = csv_converter.reverse(self.covariate_table.fullPath())
    covariate_list = []
    for subject_covariate_dict in covariate_dict.values():
      covariate_list = list(set( covariate_list + list(subject_covariate_dict.keys())))
    covariate_list.sort()
    self.signature['covariate_list'] = ListOf(Choice(*covariate_list))
    self.changeSignature(self.signature)

def updateThresholdMaskingFields( self, proc ):
  if self.threshold_masking == "Neither":
    self.setDisable('threshold_value')
  else:
    self.setEnable('threshold_value')
  self.changeSignature( self.signature )

def updateThresholdMaskingValue( self, proc ):
  if self.threshold_masking == 'Absolute':
    return 100
  elif self.threshold_masking == 'Relative':
    return 0.8

def updateGlobalCalculationFields( self, proc ):
  if self.global_calculation == 'User':
    self.setEnable('user_global_values')
  else:
    self.setDisable('user_global_values')
  self.changeSignature( self.signature )

def updateOverallGrandMeanScalingFields( self, proc ):
  if self.overall_grand_mean_scaling:
    self.setEnable('grand_mean_scaled_value')
  else:
    self.setDisable('grand_mean_scaled_value')
  self.changeSignature( self.signature )

def updateBatchPath(self, proc):
  if self.spm_workspace_directory is not None:
    return os.path.join(self.spm_workspace_directory.fullPath(), 'spm8_two_sample_ttest_job.m')

def execution(self, context):

  if os.path.exists( self.two_sample_T_test_mat_file.fullPath() ):
    os.remove(self.two_sample_T_test_mat_file.fullPath())

  two_sample_t_test = TwoSampleTTest()
  two_sample_t_test.setDirectory(self.spm_workspace_directory.fullPath())

  group_1_path_list = [group_1_diskitem.fullPath() for group_1_diskitem in self.group_1_images]
  two_sample_t_test.setGroup1Scans(group_1_path_list)
  group_2_path_list = [group_2_diskitem.fullPath() for group_2_diskitem in self.group_2_images]
  two_sample_t_test.setGroup2Scans(group_2_path_list)
  if self.independence:
    two_sample_t_test.enableIndependence()
  else:
    two_sample_t_test.disableIndependence()
  if self.variance == 'Equal':
    two_sample_t_test.setEqualVariance()
  else:
    two_sample_t_test.setUnequalVariance()
  if self.grand_mean_scaling:
    two_sample_t_test.enableGrandMeanScaling()
  else:
    two_sample_t_test.disableGrandMeanScaling()
  if self.ANCOVA:
    two_sample_t_test.enableANCOVA()
  else:
    two_sample_t_test.disableANCOVA()

  if self.threshold_masking == "Neither":
    two_sample_t_test.unsetThreshold()
  elif self.threshold_masking == 'Absolute':
    two_sample_t_test.setThresholdMethodToAbsolute()
  elif self.threshold_masking == 'Relative':
    two_sample_t_test.setThresholdMethodToRelative()

  if self.implicit_mask:
    two_sample_t_test.enableImplicitMask()
  else:
    two_sample_t_test.disableImplicitMask()

  if self.explicit_mask is not None:
    two_sample_t_test.setExplicitMask(self.explicit_mask.fullPath())

  if self.global_calculation == 'Omit':
    two_sample_t_test.setGlobalCalculationMethodToOmit()
  if self.global_calculation == 'User':
    two_sample_t_test.setGlobalCalculationMethodToUser()
    two_sample_t_test.setGlobalCalculationGlobalValues( self.user_global_values )
  if self.global_calculation == 'Mean':
    two_sample_t_test.setGlobalCalculationMethodToMean()

  if self.overall_grand_mean_scaling:
    two_sample_t_test.enableOverallGrandMeanScaling()
    two_sample_t_test.setOverallGrandMeanScalingValue(self.grand_mean_scaled_value)
  else:
    two_sample_t_test.disableOverallGrandMeanScaling()

  if self.normalisation == "Neither":
    two_sample_t_test.unsetGlobalNormalisation()
  elif self.normalisation == 'Proportional':
    two_sample_t_test.setGlobalNormalisationToProportional()
  elif self.normalisation == 'ANCOVA':
    two_sample_t_test.setGlobalNormalisationToANCOVA()

  if not None in [self.covariate_table, self.covariate_list]:
    images_diskitem_list = self.group_1_images + self.group_2_images
    covariate_list = createCovariateList(self.covariate_table, self.covariate_list, images_diskitem_list)
    for covariate in covariate_list:
      two_sample_t_test.appendCovariate(covariate)

  spm = validation()
  spm.addModuleToExecutionQueue(two_sample_t_test)
  spm.setSPMScriptPath(self.batch_location.fullPath())
  output = spm.run()
  context.log(name, html=output)

#==============================================================================
#==============================================================================
# #
#==============================================================================
#==============================================================================
def createCovariateList(covariate_table_diskitem, covariate_name_list, image_diskitem_list):
  covariate_list = []
  covariate_dict, header_id_list = csv_converter.reverse(covariate_table_diskitem.fullPath())
  subject_id_list = buildSubjectIDList(header_id_list, image_diskitem_list)

  for covariate_name in covariate_name_list:
    cov = Covariate()
    cov.setName( covariate_name )
    covariate_vector = []
    for subject_id in subject_id_list:
      if isNumber(covariate_dict[subject_id][covariate_name]):
        covariate_vector.append(covariate_dict[subject_id][covariate_name])
      else:
        raise ValueError( 'Covariable "' + covariate_name + '" not found for ' + subject_id )
    cov.setVector(covariate_vector)
    covariate_list.append(cov)
  return covariate_list

def buildSubjectIDList(header_item_list, image_diskitem_list):
  subject_id_list = []
  for image_diskitem in image_diskitem_list:
    image_hierarchy_attr = image_diskitem.hierarchyAttributes()
    subject_item_list = []
    for header_item in header_item_list:
      subject_item_list.append( image_hierarchy_attr[header_item] )
    subject_id = ';'.join(subject_item_list)
    subject_id_list.append(subject_id)
  return subject_id_list

def isNumber(number):#TODO check why we do not use numbers.Real ...
  number_str= str(number)
  abs_number_str = number_str.replace('-','')
  if abs_number_str.isdigit():
    return True
  else:
    try:
      float(abs_number_str)
      return True
    except:
      return False
