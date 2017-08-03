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
#  Run DARTEL (create Templates)
from soma.spm.spm12.tools.dartel_tools.run_dartel import RunDartel
from soma.spm.spm12.tools.dartel_tools.run_dartel.outer_iteration import OuterIteration
from soma.spm.spm12.tools.dartel_tools.run_dartel.optimisation_settings import OptimisationSettings
from soma.spm.spm12.tools.dartel_tools.run_dartel.settings import Settings

run_dartel = RunDartel()
run_dartel.setFirstImageList(['/tmp/volume_1.nii', '/tmp/volume_2.nii'])
#second images is optional
run_dartel.appendImageList(['/tmp/second_volume_1.nii', '/tmp/second_volume_2.nii'])

#By default spm prefix used, but setting custom outputs is possible
run_dartel.setOutputFlowFieldPathList(['/tmp/flow_field_1.nii', '/tmp/flow_field_2.nii'])
#By default spm prefix used, but setting custom outputs is possible
run_dartel.setOutputTemplatePathList(['/tmp/template_1.nii', '/tmp/template_2.nii'])

#"RunDartel" object have default "Settings" object but it can be replaced
settings = Settings()
settings.setRegularisationFormToLinearElasticEnergy()

first_outer_iteration = OuterIteration()
first_outer_iteration.setInnerIterationsNumber(3)
first_outer_iteration.setRegParams([4, 2, 1e-06])
first_outer_iteration.setTimeSteps(1)
first_outer_iteration.setSmoothingParameter(16)
settings.appendOuterIteration(first_outer_iteration)

#By defaut 6 OuterIteration is defined

#"Settings" object have default "OptimisationSettings" object but it can be replaced
optimisation_settings = OptimisationSettings()
optimisation_settings.setLMRegularisation(0.01)
optimisation_settings.setCycles(3)
optimisation_settings.setIterations(3)

settings.setOptimisationSettings(optimisation_settings)

run_dartel.setSettings(settings)

spm.addModuleToExecutionQueue(run_dartel)
spm.setSPMScriptPath(self.batch_location.fullPath())
spm.run()  