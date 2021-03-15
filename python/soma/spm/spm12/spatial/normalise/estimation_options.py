# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, \
                                              checkIfArgumentTypeIsStrOrUnicode
import numbers 


class EstimationOptions(object):
    def __init__(self):
        self.tpm_path = None
        self.bias_regularisation = 0.0001
        self.bias_fwhm = 60
        self.affine_regularisation = 'mni'
        self.warping_regularisation = [0, 0.001, 0.5, 0.05, 0.2] 
        self.smoothness = 0
        self.sampling = 3
    
    @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
    def setTpm(self, tpm_path):
        self.tpm_path = tpm_path    
    
    @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
    def setBiasRegularisation(self, bias_regularisation):
        if bias_regularisation >= 0 and bias_regularisation <= 10:
            self.bias_regularisation = bias_regularisation
        else:
            raise ValueError('Incorrect value for bias_regularisation')
        
    @checkIfArgumentTypeIsAllowed(numbers.Integral, 1)
    def setBiasFwhm(self, bias_fwhm):
        self.bias_fwhm = str(bias_fwhm)
    
    def unsetBiasFwhm(self, bias_fwhm):
        self.bias_fwhm = 'Inf'

    def setAffineRegularisationToEuropeanBrains(self):
        self.affine_regularisation = 'mni'

    def setAffineRegularisationToAsianBrains(self):
        self.affine_regularisation = 'eastern'

    def setAffineRegularisationToAverageSizedTemplate(self):
        self.affine_regularisation = 'subj'

    def unsetAffineRegularisation(self):
        self.affine_regularisation = ''
        
    def unsetRegularisation(self):
        self.affine_regularisation = 'none'
        
    @checkIfArgumentTypeIsAllowed(list, 1)
    def setWarpingRegularisation(self, regularisation_list):
        if len(regularisation_list) == 5:
            self.warping_regularisation = regularisation_list
        else:
            raise ValueError(
                'Warping regularisation value must be list of 5 numbers')

    @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
    def setSmoothness(self, smoothness):
        self.smoothness = smoothness

    @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
    def setSamplingDistance(self, sampling):
        self.sampling = sampling
    
    def getStringListForBatch(self):
        if self.tpm_path is None:
            raise ValueError('TPM_path is required')
              
        batch_list = []
        batch_list.append("eoptions.tpm = {'%s,1'};" %self.tpm_path)
        batch_list.append("eoptions.biasreg = %g;" %self.bias_regularisation)
        batch_list.append("eoptions.biasfwhm = %s;" %self.bias_fwhm)
        batch_list.append("eoptions.affreg = '%s';" 
                          %self.affine_regularisation)
        batch_list.append("eoptions.reg = %s;" %self.warping_regularisation)
        batch_list.append("eoptions.fwhm = %g;" %self.smoothness)
        batch_list.append("eoptions.samp = %g;" %self.sampling)
      
        return batch_list
    