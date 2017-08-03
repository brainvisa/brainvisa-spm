#==============================================================================
# The following script is an example of how use this classes
#==============================================================================

from soma.spm.spm8.stats.Contrast_manager.ContrastManager import ContrastManager
from soma.spm.spm8.stats.Contrast_manager.TContrast import TContrast
from soma.spm.spm8.stats.Contrast_manager.FContrast import FContrast
from soma.spm.spm8.stats.Contrast_manager.FContrast import FContrastVector
from soma.spm.spm8.stats.Contrast_manager.TContrastCondSessBased import TContrastCondSessBasedWithExtraRegressors
from soma.spm.spm8.stats.Contrast_manager.TContrastCondSessBased import TContrastCondSessBasedWithConditions
from soma.spm.spm8.stats.Contrast_manager.TContrastCondSessBased import ContrastEntry

import numpy

#==============================================================================
contrast_manager = ContrastManager()
contrast_manager.setMatlabFilePath('/tmp/SPM.mat')
contrast_manager.deleteExistingContrast()
#==============================================================================
t_contrast = TContrast()
t_contrast.setName('T Contrast')
t_contrast.setVector([1,2,3])
t_contrast.setReplicateOverSessions('Replicate')
#==============================================================================
f_contrast = FContrast()
f_contrast.setName('F Contrast')
f_contrast_vector = FContrastVector()
f_contrast_vector.setFContrastVector(numpy.array([1,4,7]))
f_contrast_vector_2 = FContrastVector()
f_contrast_vector_2.setFContrastVector(numpy.array([[5,8,2],[6,9,3]]))
f_contrast.appendFContrastVector(f_contrast_vector)
f_contrast.appendFContrastVector(f_contrast_vector_2)
#==============================================================================
regressors_contrast = TContrastCondSessBasedWithExtraRegressors()
regressors_contrast.setName('Regressor')
regressors_contrast.setVector([1,5,9])
regressors_contrast.setSessionVector([2,4])
#==============================================================================
condition_contrast = TContrastCondSessBasedWithConditions()
condition_contrast.setName('Conditions')
condition_contrast.setSessionVector([7, 9])
first_entry = ContrastEntry()
first_entry.setContrastWeight(1)
first_entry.setCondition(2)
first_entry.setBasisFunction(3)
first_entry.setParametricModulation(4)
first_entry.setParametricModulationOrder(5)
condition_contrast.appendContrastEntry(first_entry)
second_entry = ContrastEntry()
second_entry.setContrastWeight(10)
second_entry.setCondition(20)
second_entry.setBasisFunction(30)
second_entry.setParametricModulation(40)
second_entry.setParametricModulationOrder(50)
condition_contrast.appendContrastEntry(second_entry)
#==============================================================================
#==============================================================================
contrast_manager.appendContrast(t_contrast)
contrast_manager.appendContrast(f_contrast)
contrast_manager.appendContrast(regressors_contrast)
contrast_manager.appendContrast(condition_contrast)

contrast_manager.start(context, configuration, job_path)#context and configuration are available from Brainvisa process

