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
#  Smooth
from soma.spm.spm8.spatial.smooth import Smooth

smooth = Smooth()
smooth.setInputImagePathList(['/tmp/image_1.nii', '/tmp/image_2.nii'])
smooth.setFilenamePrefix('s')
#By default spm prefix used, but setting custom outputs is possible
smooth.setOutputImagePathList(['/tmp/image_1_smoothed.nii', '/tmp/image_2_smoothed.nii'])
smooth.setFWHM([8,8,8])
smooth.setDataTypeToInt16()
smooth.setImplicitMasking()

spm.addModuleToExecutionQueue(smooth)
spm.setSPMScriptPath('/tmp/smooth_batch.nii')
spm.run()