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
# VBM Segmentation
from soma.spm.spm8.tools.vbm import EstimateAndWrite
from soma.spm.spm8.tools.vbm.estimation_options import EstimationOptions
from soma.spm.spm8.tools.vbm.extended_options import ExtendedOptions
from soma.spm.spm8.tools.vbm.writing_options import WritingOptions, GreyMatterWritingOptions, WhiteMatterWritingOptions, CSFMatterWritingOptions, BiasCorrectedWritingOptions, PVELabelWritingOptions

estimate_and_write = EstimateAndWrite()
estimate_and_write.setVolumePath('/tmp/t1mri.nii')

est_option = EstimationOptions()
est_option.setTissueProbilityMapPath('/tmp/TPM_template.nii')
est_option.setGaussianPerClassesList([2, 2, 2, 3, 4, 2])
est_option.setBiasRegularisationToLight()
est_option.setBiasFWHMTo60cutoff()
est_option.setAffineRegularisationToEuropeanBrains()
est_option.setWarpingRegularisation(4)
est_option.setSamplingDistance(3)

ext_options = ExtendedOptions()
#choose
dartel_normalization = True
ext_options.setDartelSpatialNormalization()
ext_options.setDartelTemplatePath('/tmp/DARTEL_template.nii')
#or
dartel_normalization = False
ext_options.setSPMDefaultSpatialNormalization()

ext_options.unsetSANLMDenoising()
ext_options.setMRFWeighting(0.15)
ext_options.setCleanUpToLight()
ext_options.enableDisplayAndPrintResult()

grey_options = GreyMatterWritingOptions(dartel_normalization)
grey_options.setNative()
#By default spm prefix used, but setting custom outputs is possible
grey_options.setNativePath(/'tmp/grey_native.nii')
grey_options.unsetNormalized()
grey_options.unsetModulation()
grey_options.unsetDartelExport()

white_options = WhiteMatterWritingOptions(dartel_normalization)
white_options.unsetNative()
white_options.unsetNormalized()
white_options.unsetModulation()
white_options.unsetDartelExport()

csf_options = CSFMatterWritingOptions(dartel_normalization)
csf_options.unsetNative()
csf_options.unsetNormalized()
csf_options.unsetModulation()
csf_options.unsetDartelExport()

bias_options = BiasCorrectedWritingOptions(dartel_normalization)
bias_options.unsetNative()
bias_options.setNormalized()
#By default spm prefix used, but setting custom outputs is possible
bias_options.setNormalizedPath('/tmp/bias_njormalized.nii')
bias_options.unsetAffine()

pve_options = PVELabelWritingOptions(dartel_normalization)
pve_options.unsetNative()
pve_options.unsetNormalized()
pve_options.setDartelExportToRigid()
#By default spm prefix used, but setting custom outputs is possible
pve_options.setDartelRigidPath('/tmp/pve_dartel.nii')

wri_options = WritingOptions(dartel_normalization)
wri_options.discardJacobianNormalized()
wri_options.discardDeformationField()
#By default spm prefix used, but setting custom outputs is possible
wri_options.setMatterVolumesPath('/tmp/GM_WM_CSF_volumes.txt')


wri_options.replaceGreyMatterWritingOptions(grey_options)
wri_options.replaceWhiteMatterWritingOptions(white_options)
wri_options.replaceCSFMatterWritingOptions(csf_options)
wri_options.replaceBiasCorrectedWritingOptions(bias_options)
wri_options.replacePVELabelWritingOptions(pve_options)

estimate_and_write.replaceEstimationOptions(est_option)
estimate_and_write.replaceExtendedOptions(ext_options)
estimate_and_write.replaceWritingOptions(wri_options)
  
spm.addModuleToExecutionQueue(estimate_and_write)
spm.setSPMScriptPath(self.batch_location.fullPath())
spm.run()       