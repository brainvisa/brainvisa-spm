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
#  Coregister : Estimate & Reslice

from soma.spm.spm8.spatial.coregister.reslice_options import ResliceOptions
from soma.spm.spm8.spatial.coregister.estimation_options import EstimationOptions
from soma.spm.spm8.spatial.coregister import EstimateAndReslice

estimation_options = EstimationOptions()
#already initialize with spm defaults but to modify it, follow this example:
estimation_options.setObjectiveFunctionToMutualInformation()

estimation_options.setSeparation([4,2])
estimation_options.setTolerances([0.02,  0.02,  0.02, 0.001, 0.001, 0.001,  0.01,  0.01,  0.01, 0.001, 0.001, 0.001])
estimation_options.setHistogramSmoothing([7,7])

reslice_options = ResliceOptions()
#already initialize with spm defaults but to modify it, follow this example:
reslice_options.setInterpolationToNearestNeighbour()
reslice_options.setWrapping(False, False, False)# "No wrap" (X, Y, Z)
reslice_options.setMasking()
reslice_options.setFilenamePrefix('r')

estimate_and_reslice = EstimateAndReslice()
estimate_and_reslice.setReferenceVolumePath('/tmp/reference.nii')
estimate_and_reslice.setSourceVolumePath('/tmp/source.nii')
#optional other volumes:
estimate_and_reslice.setOtherVolumesPathList(['/tmp/other_1.nii', '/tmp/other_2.nii'])
#By default spm prefix used, but setting custom outputs is possible
estimate_and_reslice.setSourceWarpedPath('/tmp/source_warped.nii')
#optional : 
estimate_and_reslice.setOtherVolumesWarpedPathList(['/tmp/other_1_warped.nii','/tmp/other_2_warped.nii'])


estimate_and_reslice.replaceEstimationOptions(estimation_options)#already exists with spm defauts values(useless if spm default used)
estimate_and_reslice.replaceResliceOptions(reslice_options)#already exists with spm defauts values(useless if spm default used)
estimate_and_reslice.start(configuration, '/tmp/batch_coregister.m')#configuration is BV object (containing SPM & Matlab paths)

#===============================================================================
#  Coregister : Estimate Only
from soma.spm.spm8.spatial.coregister.estimation_options import EstimationOptions
from soma.spm.spm8.spatial.coregister import Estimate
from soma.spm.spm_launcher import SPM8, SPM8Standalone

estimation_options = EstimationOptions()
#already initialize with spm defaults but to modify it, follow this example:
estimation_options.setObjectiveFunctionToMutualInformation()

estimation_options.setSeparation([4,2])
estimation_options.setTolerances([0.02,  0.02,  0.02, 0.001, 0.001, 0.001,  0.01,  0.01,  0.01, 0.001, 0.001, 0.001])
estimation_options.setHistogramSmoothing([7,7])


estimate = Estimate()
estimate.setReferenceVolumePath('/tmp/reference.nii')
estimate.setSourceVolumePath('/tmp/source.nii')

estimate.setOtherVolumesPathList(['/tmp/other_1.nii', '/tmp/other_2.nii'])

estimate.replaceEstimationOptions(estimation_options)#already exists with spm defauts values(useless if spm default used)

spm.addModuleToExecutionQueue(estimation_options)
spm.setSPMScriptPath('/tmp/batch_coregister.m')
spm.run()