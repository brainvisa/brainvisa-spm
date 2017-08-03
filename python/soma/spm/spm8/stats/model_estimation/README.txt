#==============================================================================
# The following script is an example of how use this classes
#==============================================================================
#==============================================================================

#===============================================================================
# I) ModelEstimationClassical
#===============================================================================
from soma.spm.spm8.stats.Model_estimation.ModelEstimation import ModelEstimationClassical

classical_estimation = ModelEstimationClassical()
#-----------common part for all Estimation model-----------------------
classical_estimation.setMatlabFilePath('/tmp/SPM.mat')
classical_estimation.start(context, configuration, job_path)#context and configuration are available from Brainvisa process
#----------------------------------------------------------------------

#===============================================================================
# II) ModelEstimationBayesianSecondLevel
#===============================================================================
from soma.spm.spm8.stats.Model_estimation.ModelEstimation import ModelEstimationBayesianSecondLevel

bayesian_second_level_estimation = ModelEstimationBayesianSecondLevel()
#-----------common part for all Estimation model-----------------------
bayesian_second_level_estimation.setMatlabFilePath('/tmp/SPM.mat')
bayesian_second_level_estimation.start(context, configuration, job_path)#context and configuration are available from Brainvisa process
#----------------------------------------------------------------------

#===============================================================================
# III) ModelEstimationBayesianFirstLevel
#===============================================================================
from soma.spm.spm8.stats.Model_estimation.ModelEstimation import ModelEstimationBayesianFirstLevel

bayesian_first_level_estimation = ModelEstimationBayesianFirstLevel()
bayesian_first_level_estimation.setAnalysisSpace(analysis_space)#analysis_space must be AnalysisSpaceVolume, AnalysisSpaceSlices or AnalysisSpaceClusters object
bayesian_first_level_estimation.setSignalPriors('UGL')#possible signals priors are 'UGL', 'GMRF', 'LORETA', 'WGL', 'Global', 'Uninformative'
bayesian_first_level_estimation.setARModelOrderVector([3])
bayesian_first_level_estimation.setNoisePriors(possible_noise_priors)#possible noise priors are 'UGL', 'GMRF', 'LORETA', 'Tissue-type', 'Robust'('UGL' by default)
if possible_noise_priors == 'Tissue-type':
  bayesian_first_level_estimation.setTissueTypePath('/tmp/tissue.nii')#only use if possible_noise_priors == 'Tissue-type', and necessary in this case
bayesian_first_level_estimation.computeLogEvidenceMap()#or doNotComputeLogEvidenceMap
bayesian_first_level_estimation.enableFirstLevelANOVA()#or disableFirstLevelANOVA
bayesian_first_level_estimation.enableSecondLevelANOVA()#or disableSecondLevelANOVA
bayesian_first_level_estimation.appendSimpleContrast(simple_contrast)#or setSimpleContrastList(simple_contrast_list) # simple_contrast must be SimpleContrast object

#-----------common part for all Estimation model-----------------------
bayesian_first_level_estimation.setMatlabFilePath('/tmp/SPM.mat')
bayesian_first_level_estimation.start(context, configuration, job_path)#context and configuration are available from Brainvisa process
#----------------------------------------------------------------------

#===============================================================================
# AnalysisSpaceVolume(AnalysisSpace)
#===============================================================================
from soma.spm.spm8.stats.Model_estimation.AnalysisSpace import AnalysisSpaceVolume

analysis_space_volume = AnalysisSpaceVolume()

#===============================================================================
# AnalysisSpaceSlices(AnalysisSpace)
#===============================================================================
from soma.spm.spm8.stats.Model_estimation.AnalysisSpace import AnalysisSpaceSlices

analysis_space_slices = AnalysisSpaceSlices()
analysis_space_slices.setSliceNumberList([1])#An X-by-1 array must be entered

#===============================================================================
# AnalysisSpaceClusters(AnalysisSpace)
#===============================================================================
from soma.spm.spm8.stats.Model_estimation.AnalysisSpace import AnalysisSpaceClusters

analysis_space_clusters = AnalysisSpaceClusters()
analysis_space_clusters.setClusterMask('/tmp/cluster_mask.nii')

#===============================================================================
# SimpleContrast
#===============================================================================
from soma.spm.spm8.stats.Model_estimation.SimpleContrast import SimpleContrast

simple_contrast = SimpleContrast()
simple_contrast.setName('contrast')
simple_contrast.setVector([1,-1])
