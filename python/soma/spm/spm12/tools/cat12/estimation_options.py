from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsStrOrUnicode
import numbers

class EstimationOptions(object):
    """"[summary]"

    Parameters
    ----------
    object : [type]
        [description]
    """
    def __init__(self):
        self.tissue_probility_map_path = None
        self.affine_regularisation = "mni"
        self.inhomogeneity_correction = "0.5"
        self.processing_accuracy = "0.5"
        
    @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
    def set_tissue_proba_map_path(self, tissue_probility_map_path):
        self.tissue_probility_map_path = tissue_probility_map_path
    
    # Affine regularisation
    def set_affine_regularisation_EuropeanBrains(self):
        self.affine_regularisation = 'mni'
        
    def set_affine_regularisation_AsianBrains(self):
        self.affine_regularisation = 'eastern'
        
    # def set_affine_regularisation_to_AverageSizedTemplate(self):
    #     self.affine_regularisation = 'subj'
        
    # def set_affine_regularisation_rigid(self):
    #     self.affine_regularisation = 'rigid'
        
    def unset_affine_regularisation(self):
        self.affine_regularisation = ''
        
    def unset_regularisation(self):
        self.affine_regularisation = 'none'
    
    # Inhomogeneity correction
    def set_inhomogeneity_correction_ultralight(self):
        self.inhomogeneity_correction = 'eps'
    
    def set_inhomogeneity_correction_light(self):
        self.inhomogeneity_correction = '0.25'
    
    def set_inhomogeneity_correction_medium(self):
        self.inhomogeneity_correction = '0.5'
    
    def set_inhomogeneity_correction_strong(self):
        self.inhomogeneity_correction = '0.75'
    
    def set_inhomogeneity_correction_heavy(self):
        self.inhomogeneity_correction = '1.0'
    
    # Processing accuracy
    def set_processing_average(self):
        self.processing_accuracy = '0.5'
    
    def set_processing_high(self):
        self.processing_accuracy = '0.75'
    
    def set_processing_ultra_high(self):
        self.processing_accuracy = '1'
    
    def getStringListForBatch(self):
        if self.tissue_probility_map_path is not None:
            batch_list = []
            batch_list.append("opts.tpm = {'%s'};" % self.tissue_probility_map_path)
            batch_list.append("opts.affreg = '%s';" % self.affine_regularisation)
            batch_list.append("opts.biasstr = %s;" % self.inhomogeneity_correction)
            batch_list.append("opts.accstr = %s;" % self.processing_accuracy)
            return batch_list
        else:
            raise ValueError('TPM path is required')
