#==============================================================================
# The following script is an example of how use this classes
#==============================================================================
#==============================================================================

from soma.spm.spm8.stats.Results_report.ResultsReport import ResultsReport
from soma.spm.spm8.stats.Results_report.ContrastQuery import ContrastQuery
from soma.spm.spm8.stats.Results_report.Masking import Masking


result = ResultsReport()
result.setMatlabFilePath('/tmp/SPM.mat')

contrast_1 = ContrastQuery()
contrast_1.setTitle( 'first contrast')
contrast_1.setContrastIndexList([1])
contrast_1.setFWEThreshold()#or unsetThreshold()
contrast_1.setThresholdValue(0.05)
contrast_1.setExtentValue(0)

masking = Masking()
masking.setContrastIndexList([5])
masking.setMaskThreshold(0.05)
masking.enableExclusiveMask()#or enableInclusiveMask

contrast_1.setMasking(masking)

contrast_2 = ContrastQuery()
contrast_2.setTitle( 'second contrast')
contrast_2.setContrastIndexList([6, 7])
contrast_2.setExtentValue(0)
contrast_2.unsetThreshold()# or setFWEThreshold

result.appendContrastQuery( contrast_1 )
result.appendContrastQuery( contrast_2 )
#or result.setContrastQueryList([contrast_1, contrast_2])

result.setDataTypeOnVolumetric()# or setDataTypeOnScalpTime, setDataTypeOnScalpFrequency, setDataTypeOnTimeFrequency, setDataTypeOnFrequencyFrequency

result.enablePrintResult()#or disablePrintResult

print result.getBatchScript()
