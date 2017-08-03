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
#  ContrastManager
from soma.spm.spm8.stats.contrast_manager import ContrastManager
from soma.spm.spm8.stats.contrast_manager.tcontrast import TContrast
from soma.spm.spm8.stats.contrast_manager.fcontrast import FContrast, FContrastVector
from soma.spm.spm8.stats.contrast_manager.tcontrast_condsessbased import TContrastCondSessBased#useless but exists

contrast_manager = ContrastManager()
contrast_manager.setMatlabFilePath('/tmp/spm.mat')
contrast_manager.deleteExistingContrast()
#to add new TContrast:
T_contrast = TContrast()
T_contrast.setName('contrast_t')
T_contrast.setVector([...])
T_contrast.setReplicateOverSessions(