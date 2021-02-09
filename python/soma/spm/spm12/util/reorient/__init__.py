from __future__ import absolute_import
import numpy as np
from soma.spm.spm_main_module import SPM12MainModule
from soma.spm.spm_batch_maker_utils import moveSPMPath
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode


class Reorient(SPM12MainModule):
    """
    Reorient images given a set of parameters.
    The reorientation parameters can be given either as a 4x4 matrix or as parameters as defined for
    spm matrix.m. The new image orientation will be computed by PRE-multiplying the original orientation
    matrix with the supplied matrix.
    
    This branch contains 3 items:
    * Images to reorient
    * Reorient by
    * Filename Prefix
    """
    
    def __init__(self):
        self.images_path_list = []
        
        self.reorient_by = 'reorient_matrix'
        self.reorient_matrix = [[1, 0, 0, 0],
                                [0, 1, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]]  # 4x4
        self.reorient_parameters = [0, 0, 0, 0, 0, 0,
                                    1, 1, 1, 0, 0, 0]  # 1x12
        self.saved_matrix_path = ''
        
        self.prefix = ''
        
        self.output_images_path_list = []
    
    def set_images_path_list(self, path_list):
        if isinstance(path_list, str):
            self.images_path_list = [path_list]
        elif isinstance(path_list, list):
            self.images_path_list = path_list
        else:
            raise ValueError("Images path has to be a list or a string")
    
    def set_reorient_by_reorient_matrix(self):
        self.reorient_by = 'reorient_matrix'
    
    def set_reorient_by_reorient_parameters(self):
        self.reorient_by = 'reorient_parameters'
    
    def set_reorient_by_saved_matrix(self):
        self.reorient_by = 'saved_matrix'
    
    @checkIfArgumentTypeIsAllowed(list, 1)
    def set_reorient_matrix(self, mat):
        if np.array(mat).shape == (4, 4):
            self.reorient_matrix = [[str(val) for val in line] for line in mat]
        else:
            raise ValueError("Reorient matrix have to be [4 x 4] matrix")
    
    @checkIfArgumentTypeIsAllowed(list, 1)
    def set_reorient_parameters(self, param):
        if np.array(param).shape == (12,):
            self.reorient_parameters = [str(p) for p in param]
        else:
            raise ValueError("Reorient parameters have to be [12 x 1] array")

    @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
    def set_saved_matrix(self, path):
        self.saved_matrix_path = path
    
    @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
    def set_prefix(self, pref):
        self.prefix = pref
    
    def set_output_images_path_list(self, path_list):
        if isinstance(path_list, str):
            self.output_images_path_list = [path_list]
        elif isinstance(path_list, list):
            self.output_images_path_list = path_list
        else:
            raise ValueError("Images path has to be a list or a string")
    
    def getStringListForBatch(self):
        batch_list = []
        if self.images_path_list:
            batch_im_list = ["'%s,1'" % i for i in self.images_path_list]
            batch_list.append("spm.util.reorient.srcfiles = {%s};" % '\n'.join(batch_im_list))
            
            if self.reorient_by == 'reorient_matrix':
                matrix = "\n".join([' '.join(line) for line in self.reorient_matrix])
                batch_list.append("spm.util.reorient.transform.transM = [%s];" % matrix)
            elif self.reorient_by == 'reorient_parameters':
                params = " ".join(self.reorient_parameters)
                batch_list.append("spm.util.reorient.transform.transprm = [%s];" % params)
            elif self.reorient_by == 'saved_matrix':
                batch_list.append("spm.util.reorient.transform.transF = {'%s'};" % self.saved_matrix_path)
    
            batch_list.append("spm.util.reorient.prefix = '%s';" % self.prefix)
            
            return batch_list
        else:
            raise ValueError('At least one image path is required')

    def _moveSPMDefaultPathsIfNeeded(self):
        if self.output_images_path_list is not None:
            if len(self.images_path_list) == len(self.output_images_path_list):
                for input_path, output_path in zip(
                   self.images_path_list, self.output_images_path_list):
                    moveSPMPath(input_path,
                                output_path,
                                prefix=self.prefix)
            else:
                raise ValueError(
                    'Input and output path_list do not have the same length.')
        else:
            # Default prefix used
            pass
      