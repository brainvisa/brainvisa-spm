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
#  Create warped
from soma.spm.spm8.tools.dartel_tools.create_warped import CreateWarped

create_warped = CreateWarped()
create_warped.setFlowFieldPathList(['/tmp/flowfield_1.nii', '/tmp/flowfield_2.nii'])
create_warped.setFirstImagePathList(['/tmp/volume_1.nii', '/tmp/volume_2.nii'])
#second images is optional
create_warped.appendImageList(['/tmp/second_volume_1.nii', '/tmp/second_volume_2.nii'])
#By default spm prefix used, but setting custom outputs is possible
create_warped.setListOutputWarpedPathList([['/tmp/volume_1_warped.nii', '/tmp/volume_2_warped.nii'],
                                           ['/tmp/second_volume_1_warped.nii', '/tmp/second_volume_2_warped.nii']])

create_warped.setModulation()
create_warped.setTimeSteps(64)
create_warped.setInterpolationToNearestNeighbour()

spm.addModuleToExecutionQueue(create_warped)
spm.setSPMScriptPath(self.batch_location.fullPath())
spm.run()  