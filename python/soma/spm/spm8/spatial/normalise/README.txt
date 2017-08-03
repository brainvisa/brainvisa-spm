# HOW TO USE
#===============================================================================
# Start or call SPM instance (spm is singleton object)
from soma.spm.spm_launcher import SPM8, SPM8Standalone
spm = SPM8Standalone(spm_standalone_command,
                     spm_standalone_mcr_path,
                     spm_standalone_path)
# or
spm = SPM8(spm_path,
           matlab.executable,
           matlab.options)
#===============================================================================
#  Normalise: Estimate & Write
from soma.spm.spm8.spatial.normalise import EstimateAndWrite
from soma.spm.spm8.spatial.normalise.subject import SubjectToEstimateAndWrite
from soma.spm.spm8.spatial.normalise.writing_options import WritingOptions
from soma.spm.spm8.spatial.normalise.estimation_options import EstimationOptions
import numpy

estimate_and_write = EstimateAndWrite()
  
subject = SubjectToEstimateAndWrite()
subject.setSourceImage('/tmp/volume_1.nii')
#optional Weighting Image
subject.setSourceWeightingImage('/tmp/weighting.nii')
subject.setImageListToWrite(['/tmp/volume_1.nii', '/tmp/volume_2.nii'])
subject.setImageListWritten(['/tmp/volume_1_normalised.nii', '/tmp/volume_2_normalised.nii'])
  
estimate_and_write.appendSubject(subject)
#"EstimateAndWrite" object have default "EstimationOptions" object but it can be replaced
estimate = EstimationOptions()
estimate.setTemplateImage("/tmp/template.nii")
#optional Weighting Image
estimate.setTemplateWeightingImage(('/tmp/template_weighting.nii')
estimate.setSourceImageSmoothing(8)
estimate.setTemplateImageSmoothing(0)
estimate.setAffineRegularisationToICBMSpaceTemplate()
estimate.setNonLinearFrequencyCutOff(25)
estimate.setNonLinearIterations(16)
estimate.setNonLinearRegularisation(1)
  
estimate_and_write.replaceEstimateOptions(estimate)
  
#"EstimateAndWrite" object have default "writing" object but it can be replaced
writing = WritingOptions()
writing.setBoundingBox(numpy.array([[-78, -112, -50],[78, 76, 85]]))
writing.setVoxelSize([2,2,2])
writing.setInterpolationToNearestNeighbour()
writing.setWrapping(False, False, False)#"No wrap"
writing.setFilenamePrefix('w')

estimate_and_write.replaceWrintingOptions(writing)

spm.addModuleToExecutionQueue(estimate_and_write)
spm.setSPMScriptPath('/tmp/batch_normalise_estimate_and_write.m')
spm.run()