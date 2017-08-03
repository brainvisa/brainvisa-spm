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
from soma.spm import csv_converter
from soma.spm.spm8.stats.factorial_design import OneSampleTTest
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
name = 'spm8 - One sample T-test - generic'

signature = Signature(
  #design
  'images_are_parametric', Boolean(),
  'images', ListOf( ReadDiskItem( '4D Volume', ['NIFTI-1 image', 'SPM image', 'MINC image'] ) ),
  #Covariates
  'covariate_table', ReadDiskItem('Covariate table for SPM', 'CSV file'),
  'nuisance_covariate_list', ListOf(Choice()),
  'interest_covariate_list', ListOf(Choice()),
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
  'one_sample_T_test_mat_file', WriteDiskItem( 'Matlab SPM file', 'Matlab file' ),
  #job_batch_file
  'batch_location', WriteDiskItem( 'Matlab SPM script', 'Matlab script' ),
)

def initialization( self ):
  self.setDisable('threshold_value', 'user_global_values', 'grand_mean_scaled_value')
  self.setUserLevel(1, 'one_sample_T_test_mat_file')

  self.addLink(None, 'images_are_parametric', self.updateSignatureAboutParametricImages)
  self.addLink(None, 'covariate_table', self.updateCovariate)
  self.addLink('interest_covariate_list', 'covariate_table', self.updateCovariate)
  self.addLink( None, 'threshold_masking', self.updateThresholdMaskingFields )
  self.addLink( 'threshold_value', 'threshold_masking', self.updateThresholdMaskingValue )

  self.addLink( None, 'global_calculation', self.updateGlobalCalculationFields )

  self.addLink( None, 'overall_grand_mean_scaling', self.updateOverallGrandMeanScalingFields )

  self.addLink("batch_location", "spm_workspace_directory", self.updateBatchPath)

  self.setOptional( 'covariate_table', 'nuisance_covariate_list', 'interest_covariate_list', 'explicit_mask' )


  self.grand_mean_scaling = False
  self.ancova = False
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
    nuisance_covariate_list = []
    for subject_covariate_dict in covariate_dict.values():
      nuisance_covariate_list = list(set( nuisance_covariate_list + subject_covariate_dict.keys()))
    nuisance_covariate_list.sort()
    self.signature['nuisance_covariate_list'] = ListOf(Choice(*nuisance_covariate_list))
    self.signature['interest_covariate_list'] = ListOf(Choice(*nuisance_covariate_list))
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
    return os.path.join(self.spm_workspace_directory.fullPath(), 'spm8_one_sample_ttest_job.m')

def execution(self, context):

  if os.path.exists( self.one_sample_T_test_mat_file.fullPath() ):
    os.remove(self.one_sample_T_test_mat_file.fullPath())

  one_sample_t_test = OneSampleTTest()
  one_sample_t_test.setDirectory(self.spm_workspace_directory.fullPath())

  images_path_list = [diskitem.fullPath() for diskitem in self.images]
  one_sample_t_test.setScans(images_path_list)


  if self.threshold_masking == "Neither":
    one_sample_t_test.unsetThreshold()
  elif self.threshold_masking == 'Absolute':
    one_sample_t_test.setThresholdMethodToAbsolute()
  elif self.threshold_masking == 'Relative':
    one_sample_t_test.setThresholdMethodToRelative()

  if self.implicit_mask:
    one_sample_t_test.enableImplicitMask()
  else:
    one_sample_t_test.disableImplicitMask()

  if self.explicit_mask is not None:
    one_sample_t_test.setExplicitMask(self.explicit_mask.fullPath())

  if self.global_calculation == 'Omit':
    one_sample_t_test.setGlobalCalculationMethodToOmit()
  if self.global_calculation == 'User':
    one_sample_t_test.setGlobalCalculationMethodToUser()
    one_sample_t_test.setGlobalCalculationGlobalValues( self.user_global_values )
  if self.global_calculation == 'Mean':
    one_sample_t_test.setGlobalCalculationMethodToMean()

  if self.overall_grand_mean_scaling:
    one_sample_t_test.enableOverallGrandMeanScaling()
    one_sample_t_test.setOverallGrandMeanScalingValue(self.grand_mean_scaled_value)
  else:
    one_sample_t_test.disableOverallGrandMeanScaling()

  if self.normalisation == "Neither":
    one_sample_t_test.unsetGlobalNormalisation()
  elif self.normalisation == 'Proportional':
    one_sample_t_test.setGlobalNormalisationToProportional()
  elif self.normalisation == 'ANCOVA':
    one_sample_t_test.setGlobalNormalisationToANCOVA()

  if self.covariate_table is not None:
    covariate_name_list = []
    if self.nuisance_covariate_list is not None:
      covariate_name_list.extend(self.nuisance_covariate_list)
    if self.interest_covariate_list is not None:
      covariate_name_list.extend(self.interest_covariate_list)
    covariate_list = createCovariateList(self.covariate_table, covariate_name_list, self.images)

    for covariate in covariate_list:
      one_sample_t_test.appendCovariate(covariate)

  spm = validation()
  spm.addModuleToExecutionQueue(one_sample_t_test)
  spm.setSPMScriptPath(self.batch_location.fullPath())
  output = spm.run()
  context.log(name, html=output)

#==============================================================================
#==============================================================================
# #
#==============================================================================
#==============================================================================
def createCovariateList(covariate_table_diskitem, covariate_name_list, image_diskitem_list):
  nuisance_covariate_list = []
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
    nuisance_covariate_list.append(cov)
  return nuisance_covariate_list

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

def isNumber(number):
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
