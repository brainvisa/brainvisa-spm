# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.spatial.normalise.writing_options \
    import WritingOptions as WritingOptions_virtual
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.spm_batch_maker_utils import convertNumpyArrayToSPMString, \
                                           convertlistToSPMString

import numpy
import numbers 

 
class WritingOptions(WritingOptions_virtual):
    def __init__(self):
        self.bounding_box = numpy.array([[-78, -112, -70],[78, 76, 85]])
        self.voxel_size = [2, 2, 2]
        self.interpolation = 1
        self.filename_prefix = 'w'

    @checkIfArgumentTypeIsAllowed(numbers.Integral, 1)
    def setInterpolation(self, interpolation):
        if interpolation >= 0 and interpolation <= 7:
            self.interpolation = interpolation
        else:
            raise ValueError('Incorrect value for interpolation')
    
    def getStringListForBatch(self):
        batch_list = []
        batch_list.append('woptions.bb = %s;' 
                          %convertNumpyArrayToSPMString(self.bounding_box))
        batch_list.append('woptions.vox = %s;' 
                          %convertlistToSPMString(self.voxel_size))
        batch_list.append('woptions.interp = %i;' %self.interpolation)
        batch_list.append("woptions.prefix = '%s';" %self.filename_prefix)
        
        return batch_list
