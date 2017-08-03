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
# High-Dimensional Warping
from soma.spm.spm8.tools.hdw import HDW
from soma.spm.spm8.tools.hdw.subject import Subject
from soma.spm.spm8.tools.hdw.bias_correction_options import BiasCorrectionOptions
from soma.spm.spm8.tools.hdw.warping_options import WarpingOptions


hdw = HDW()

subject = Subject()
subject.setReferenceImage('/tmp/reference.nii')
subject.setMovedImage('/tmp/moved.nii')
#By default spm prefix used, but setting custom outputs is possible
subject.setOutputDeformationFieldPath('/tmp/deformation_field.nii')
#By default spm prefix used, but setting custom outputs is possible
subject.setOutputJacobianDeterminantPath('/tmp/jacobian.nii')

hdw.appendSubject(subject)

#"HDW" object have default "BiasCorrectionOptions" object but it can be replaced
bias_correction = BiasCorrectionOptions()
bias_correction.setIterations(8)
bias_correction.setBiasFWHMTo60mmCutoff()
bias_correction.setBiasRegularisationToMedium()
bias_correction.setLMRegularisationToMedium()

hdw.replaceBiasCorrectionOptions(bias_correction)

#"HDW" object have default "WarpingOptions" object but it can be replaced
warping = WarpingOptions()
warping.setIterations(8)
warping.setWarpingRegularisation(4)

hdw.replaceWarpingOptions(warping)

spm.addModuleToExecutionQueue(hdw)
spm.setSPMScriptPath(self.batch_location.fullPath())
spm.run()    