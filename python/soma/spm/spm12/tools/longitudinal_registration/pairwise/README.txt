# HOW TO USE
#===============================================================================
# Start or call SPM instance (spm is singleton object)
from soma.spm.spm_launcher import SPM12, SPM12Standalone
spm = SPM12Standalone(spm_standalone_command,
                      spm_standalone_mcr_path,
                      spm_standalone_path)
# or
spm = SPM12(spm_path,
            matlab.executable,
            matlab.options)
#===============================================================================
#  pairwaise
from soma.spm.spm12.tools.longitudinal_registration.pairwise import PairwiseLongitudinalRegistration
import numpy

pairwise = PairwiseLongitudinalRegistration()

pairwise.setTime1Volumes([/tmp/volume_1.nii'])
pairwise.setTime2Volumes(['/tmp/volume_2.nii'])
pairwise.setTimeDifference([1])
pairwise.setNoiseEstimateToNaN() or pairwise.setNoiseEstimate(numpy.array(...))
pairwise.setWarpingRegulariation([0, 0, 100, 25, 100])
pairwise.setBiasRegularisation(1000000)
pairwise.saveMidPointAverage()
#By default spm prefix used, but setting custom outputs is possible
pairwise.setOutputMidPointAverage(['/tmp/volume_mid_point_1.nii'])
pairwise.discardJacobianRate()
pairwise.discardDivergenceRate()
pairwise.saveDeformationFields()
#By default spm prefix used, but setting custom outputs is possible
pairwise.setOutputTime1VolumeDeformationField([/tmp/volume_1_deformation_field.nii'])
pairwise.setOutputTime2VolumeDeformationField([/tmp/volume_2_deformation_field.nii'])

spm.addModuleToExecutionQueue(pairwise)
spm.setSPMScriptPath('/tmp/batch_pairwise.m')
spm.run()