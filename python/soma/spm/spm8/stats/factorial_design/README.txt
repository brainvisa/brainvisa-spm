#==============================================================================
# The following script is an example of how use this classes
#==============================================================================
from soma.spm.spm8.stats.Factoriel_design.FactorielDesign import PairedTTest, OneSampleTTest, TwoSampleTTest
from soma.spm.spm8.stats.Factoriel_design.Covariate import Covariate
#==============================================================================
#==============================================================================


#==============================================================================
# Covariate
#==============================================================================
cov = Covariate()
cov.setName( 'cov_name' )
cov.setVector([1,-1])
cov.setInteraction('None')#possible interactions are 'None', 'With Factor 1', 'With Factor 2', 'With Factor 3'
cov.setCentering('Overall mean')#possible centering are 'Factor 3 mean', 'User specified value', 'Overall mean', 'Factor 2 mean', 'No centering', 'GM', 'As implied by ANCOVA', 'Factor 1 mean'
cov.getBatchScript()#this method is not called directly by the user(with standard using)

#==============================================================================
# Paired T Test
#==============================================================================
paired_t_test = PairedTTest()
for first_scan_path, second_scan_path in zip( first_scan_path_list, second_scan_path_list ):
  paired_t_test.addScansPair( [first_scan_path, second_scan_path])
paired_t_test.enableGrandMeanScaling()#or disableGrandMeanScaling
paired_t_test.enableANCOVA()# or disableANCOVA

#-----------common part for all Factoriel design-----------------------
paired_t_test.setDirectory('/tmp/')
paired_t_test.unsetThreshold()#or setAbsoluteThresholdMethod, setRelativeThresholdMethod
paired_t_test.enableImplicitMask()#or disableImplicitMask
paired_t_test.setExplicitMask('/tmp/explicit_mask.nii')#optional
paired_t_test.setGlobalCalculationMethod(global_calculation_method)# global_calculation_method can be 'Omit', 'User' or 'Mean'
if global_calculation_method == 'User':
  paired_t_test.setValuesForUserGlobalCalculationMethod( user_global_values )#user_global_values must be list of float
paired_t_test.enableOverallGrandMeanScaling()#or disableOverallGrandMeanScaling
paired_t_test.setOverallGrandMeanScalingValue([50])#only usefull with "enableOverallGrandMeanScaling"
paired_t_test.unsetGlobalNormalisation()#or setProportionalGlobalNormalisation, setANCOVAGlobalNormalisation
paired_t_test.setCovariateList(covariate_list)#list of "Covariate" object
paired_t_test.getBatchScript()
#----------------------------------------------------------------------

#==============================================================================
# One Sample T Test
#==============================================================================
one_sample_t_test = OneSampleTTest()

one_sample_t_test.setScans(scans_path_list)

#-----------common part for all Factoriel design-----------------------
one_sample_t_test.setDirectory('/tmp/')
one_sample_t_test.unsetThreshold()#or setAbsoluteThresholdMethod, setRelativeThresholdMethod
one_sample_t_test.enableImplicitMask()#or disableImplicitMask
one_sample_t_test.setExplicitMask('/tmp/explicit_mask.nii')#optional
one_sample_t_test.setGlobalCalculationMethod(global_calculation_method)# global_calculation_method can be 'Omit', 'User' or 'Mean'
if global_calculation_method == 'User':
  one_sample_t_test.setValuesForUserGlobalCalculationMethod( user_global_values )#user_global_values must be list of float
one_sample_t_test.enableOverallGrandMeanScaling()#or disableOverallGrandMeanScaling
one_sample_t_test.setOverallGrandMeanScalingValue([50])#only usefull with "enableOverallGrandMeanScaling"
one_sample_t_test.unsetGlobalNormalisation()#or setProportionalGlobalNormalisation, setANCOVAGlobalNormalisation
one_sample_t_test.setCovariateList(covariate_list)#list of "Covariate" object
one_sample_t_test.getBatchScript()
#----------------------------------------------------------------------

#==============================================================================
# Two Sample T Test
#==============================================================================
two_sample_t_test = TwoSampleTTest()
two_sample_t_test.setGroup1Scans(group_1_scan_path_list)
two_sample_t_test.setGroup2Scans(group_2_scan_path_list)
two_sample_t_test.enableIndependence()#or disableIndependence
two_sample_t_test.setEqualVariance()# or setUnequalVariance
two_sample_t_test.enableGrandMeanScaling()# or disableGrandMeanScaling
two_sample_t_test.enableANCOVA()# or disableANCOVA

#-----------common part for all Factoriel design-----------------------
two_sample_t_test.setDirectory('/tmp/')
two_sample_t_test.unsetThreshold()#or setAbsoluteThresholdMethod, setRelativeThresholdMethod
two_sample_t_test.enableImplicitMask()#or disableImplicitMask
two_sample_t_test.setExplicitMask('/tmp/explicit_mask.nii')#optional
two_sample_t_test.setGlobalCalculationMethod(global_calculation_method)# global_calculation_method can be 'Omit', 'User' or 'Mean'
if global_calculation_method == 'User':
  two_sample_t_test.setValuesForUserGlobalCalculationMethod( user_global_values )#user_global_values must be list of float
two_sample_t_test.enableOverallGrandMeanScaling()#or disableOverallGrandMeanScaling
two_sample_t_test.setOverallGrandMeanScalingValue([50])#only usefull with "enableOverallGrandMeanScaling"
two_sample_t_test.unsetGlobalNormalisation()#or setProportionalGlobalNormalisation, setANCOVAGlobalNormalisation
two_sample_t_test.setCovariateList(covariate_list)#list of "Covariate" object
two_sample_t_test.getBatchScript()
#----------------------------------------------------------------------
