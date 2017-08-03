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
#  serial
from soma.spm.spm12.tools.longitudinal_registration.serial import SerialLongitudinalRegistration
import numpy

serial = SerialLongitudinalRegistration()

serial.setVolumes([/tmp/volume_1.nii','/tmp/volume_2.nii'])
serial.setTimes([0,1])
serial.setNoiseEstimateToNaN() or serial.setNoiseEstimate(numpy.array(...))
serial.setWarpingRegulariation([0, 0, 100, 25, 100])
serial.setBiasRegularisation(1000000)
serial.saveMidPointAverage()
#By default spm prefix used, but setting custom outputs is possible
serial.setOutputMidPointAverage('/tmp/mid_point_average.nii')
serial.discardJacobianRate()
serial.discardDivergenceRate()
serial.saveDeformationFields()
#By default spm prefix used, but setting custom outputs is possible
serial.setOutputVolumeDeformationField(['/tmp/volume_1_deformation_field.nii', '/tmp/volume_2_deformation_field.nii'])

spm.addModuleToExecutionQueue(serial)
spm.setSPMScriptPath('/tmp/batch_serial.m')
spm.run()