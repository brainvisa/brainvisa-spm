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
#  Image calculator
from soma.spm.spm12.util.image_calculator import ImageCalculator
from soma.spm.spm12.util.image_calculator.additional_variable import AdditionalVariable
from soma.spm.spm12.util.image_calculator.options import Options

imcalc = ImageCalculator()
imcalc.setInputImagePathList([/tmp/volume_1.nii','/tmp/volume_2.nii'])
imcalc.setOutputImagePath('/tmp/output_volume.nii')
imcalc.setExpression("(i1 + i2) / first_var")

#AdditionalVariable is optional and new in spm12
var_1 = AdditionalVariable()
var_1.setName("first_var")
var_1.setValue(numpy.array(...))

imcalc.appendAdditionalVariable(var_1)

#"imcalc" object have default "options" object but it can be replaced
options = Options()
options.setDataMatrix()
options.setMaskingTypeToNoImplicitZero()
options.setInterpolationToNearestNeighbour()
options.setDataTypeToInt16()

imcalc.replaceOptions(options)

spm.addModuleToExecutionQueue(imcalc)
spm.setSPMScriptPath('/tmp/batch_imcalc.m')
spm.run()