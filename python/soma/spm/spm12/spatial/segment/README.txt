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
#  Segment

from soma.spm.spm12.spatial.segment import Segment
from soma.spm.spm12.spatial.segment.channel import Channel
from soma.spm.spm12.spatial.segment.tissue import Tissue

segment = Segment()
#===============================================================================
#The fastest way to use is using SPM defaults :
segment.setSPMDefaultSetting(['/tmp/t1mri.nii'], '/tmp/TPM_template.nii')
#or
segment.setSPMDefaultChannel(['/tmp/t1mri.nii'])
segment.setSPMDefautTissues('/tmp/TPM_template.nii')
#===============================================================================
#But each parameters can be modified
first_channel = Channel()
first_channel.setVolumePathList(['/tmp/t1mri.nii'])
#the other parameters are already set with SPM default but to modify it, follow this example:
first_channel.setBiasRegularisationToExtremelyLight()
first_channel.setBiasFWHMTo40cutoff()
first_channel.saveBiasFieldAndBiasCorrected()
#By default spm prefix used, but setting custom outputs is possible
first_channel.setBiasCorrectedPath('/tmp/t1mri_bias_corrected.nii')
first_channel.setBiasFieldPath('/tmp/t1mri_bias_field.nii')

segment.appendChannel(first_channel)

first_tissue = Tissue()
first_tissue.setTissueProbilityMapPath('/tmp/TPM_template.nii')
first_tissue.setTissueProbilityDimension(1)
first_tissue.setGaussianNumber(1)
first_tissue.setNativeTissueNativeSpace()
first_tissue.unsetWarpedTissue()
segment.appendTissue(first_tissue)

second_tissue = Tissue()
second_tissue.setTissueProbilityMapPath('/tmp/TPM_template.nii')
second_tissue.setTissueProbilityDimension(2)
second_tissue.setGaussianNumber(1)
second_tissue.setNativeTissueNativeSpace()
second_tissue.unsetWarpedTissue()
segment.appendTissue(second_tissue)

third_tissue = Tissue()
third_tissue.setTissueProbilityMapPath('/tmp/TPM_template.nii')
third_tissue.setTissueProbilityDimension(3)
third_tissue.setGaussianNumber(2)
third_tissue.setNativeTissueNativeSpace()
third_tissue.unsetWarpedTissue()
segment.appendTissue(third_tissue)

fourth_tissue = Tissue()
fourth_tissue.setTissueProbilityMapPath('/tmp/TPM_template.nii')
fourth_tissue.setTissueProbilityDimension(4)
fourth_tissue.setGaussianNumber(3)
fourth_tissue.setNativeTissueNativeSpace()
fourth_tissue.unsetWarpedTissue()
segment.appendTissue(fourth_tissue)

fifth_tissue = Tissue()
fifth_tissue.setTissueProbilityMapPath('/tmp/TPM_template.nii')
fifth_tissue.setTissueProbilityDimension(5)
fifth_tissue.setGaussianNumber(4)
fifth_tissue.setNativeTissueNativeSpace()
fifth_tissue.unsetWarpedTissue()
segment.appendTissue(fifth_tissue)

sixth_tissue = Tissue()
sixth_tissue.setTissueProbilityMapPath('/tmp/TPM_template.nii')
sixth_tissue.setTissueProbilityDimension(6)
sixth_tissue.setGaussianNumber(2)
sixth_tissue.unsetNativeTissue()
sixth_tissue.unsetWarpedTissue()
segment.appendTissue(sixth_tissue)


segment.setMRFParameter(1)
segment.setCleanUpToLight()
segment.setWarpingRegularisation([0, 0.001, 0.5, 0.05, 0.2])
segment.setAffineRegularisationToEuropeanBrains()
segment.setSmoothness(0)
segment.setSamplingDistance(3)
segment.saveDeformationFieldInverseAndForward()
segment.setDeformationFieldInverseOutputPathList('/tmp/inverse_field.nii')
segment.setDeformationFieldForwardOutputPathList('/tmp/forward_field.nii')

spm.addModuleToExecutionQueue(segment)
spm.setSPMScriptPath('/tmp/batch_segment_12.m')
spm.run()