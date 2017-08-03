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
# Deformations

from soma.spm.spm8.util.deformations import Deformations
from soma.spm.spm8.util.deformations.composition import Composition
from soma.spm.spm8.util.deformations.composition import MatFileImported
from soma.spm.spm8.util.deformations.composition import DartelFlow
from soma.spm.spm8.util.deformations.composition import DeformationField
from soma.spm.spm8.util.deformations.composition import IdentityFromImage
from soma.spm.spm8.util.deformations.composition import Identity
from soma.spm.spm8.util.deformations.composition import Inverse


deformations = Deformations()

mat_file = MatFileImported()
mat_file.setParameterFile('/tmp/spm_sn.mat")
mat_file.setVoxelSize(["NaN", "NaN", "NaN"])
mat_file.setBoundingBox(numpy.array([["NaN", "NaN", "NaN"],["NaN", "NaN", "NaN"]]))

deformations.appendDeformation(mat_file)
  
deformation_field = DeformationField()
deformation_field.setDeformationFieldPath(self.deformation_field.fullPath())
  
deformations.appendDeformation(deformation_field)

#available deformation module : DartelFlow, IdentityFromImage, Identity, Inverse, Composition

#Optional:
deformations.setCompositionName('compo')
#By default spm prefix used, but setting custom outputs is possible. Composition name is required -> "setCompositionName"
deformations.setCompositionOutputPath('/tmp/composition.nii')

deformations.setImageListToDeform(['/tmp/volume_1.nii', '/tmp/volume_2.nii'])
#By default spm prefix used, but setting custom outputs is possible.
deformations.setImageListDeformed(['/tmp/volume_1_deformed.nii', '/tmp/volume_2_deformed.nii'])

deformations.setOuputDestinationToSourceDirectories()
deformations.setInterpolationToNearestNeighbour()

spm.addModuleToExecutionQueue(deformations)
spm.setSPMScriptPath(self.batch_location.fullPath())
spm.run()    
  