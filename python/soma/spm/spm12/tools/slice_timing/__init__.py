from __future__ import absolute_import
from soma.spm.spm_main_module import SPM12MainModule
from soma.spm.spm_batch_maker_utils import moveSPMPath, convertlistToSPMString
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
import numbers


class SliceTiming(SPM12MainModule):
    
    """
    Correct differences in image acquisition time between slices.
    See http://www.fil.ion.ucl.ac.uk/spm/doc/manual.pdf#page=19
    """
    
    def __init__(self):
        self.input_path_list = None
        self.number_of_slices = None
        self.tr = None
        self.ta = None
        self.slice_order = None
        self.reference_slice_index = None
        
        self.filename_prefix = 'a'
        self.output_path_list = None
        
    @checkIfArgumentTypeIsAllowed(list, 1)
    def setInputImagesPathList(self, images_path_list):
        self.input_path_list = images_path_list        
        
    @checkIfArgumentTypeIsAllowed(numbers.Integral, 1)
    def setNumberOfSlices(self, number_of_slices):
        self.number_of_slices = number_of_slices
    
    @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
    def setRepetitionTime(self, tr):
        self.tr = tr 
    
    @checkIfArgumentTypeIsAllowed(numbers.Real, 1)
    def setAcquisitionTime(self, ta):
        self.ta = ta
    
    @checkIfArgumentTypeIsAllowed(list, 1)
    def setSliceOrder(self, slice_order):
        self.slice_order = convertlistToSPMString(slice_order)
    
    @checkIfArgumentTypeIsAllowed(numbers.Integral, 1)
    def setReferenceSliceIndex(self, reference_slice_index):
        self.reference_slice_index = reference_slice_index
    
    @checkIfArgumentTypeIsAllowed(str, 1)
    def setFilenamePrefix(self, filename_prefix):
        self.filename_prefix = filename_prefix 
        
    @checkIfArgumentTypeIsAllowed(str, 1)
    def setOuputImagePath(self, image_path):
        self.output_path_list = image_path 

    def getStringListForBatch(self):
        if None in self.input_path_list:
            raise ValueError('At least one image path is required')
        
        image_path_list_for_batch = [] 
        for image_path in self.input_path_list:
            image_path_list_for_batch.append("'%s'" % image_path) 
        image_path_batch = '\n'.join(image_path_list_for_batch)
                    
        batch_list = []
        batch_list.append(
            "spm.temporal.st.scans = {\n{\n%s\n}\n};" % image_path_batch)
        batch_list.append(
            'spm.temporal.st.nslices = %i;' % self.number_of_slices)
        batch_list.append('spm.temporal.st.tr = %.2f;' % self.tr)
        batch_list.append('spm.temporal.st.ta = %.2f;' % self.ta)
        batch_list.append('spm.temporal.st.so = %s;' % self.slice_order)
        batch_list.append(
            'spm.temporal.st.refslice = %i;' % self.reference_slice_index)
        batch_list.append('spm.temporal.st.prefix = %s' % self.filename_prefix)
        
        return batch_list
        
    def _moveSPMDefaultPathsIfNeeded(self):
        if self.output_path_list is not None:
            if len(self.input_path_list) == len(self.output_path_list):
                for input_path, output_path in zip(self.input_path_list,
                                                   self.output_path_list):
                    moveSPMPath(input_path,
                                output_path,
                                prefix=self.filename_prefix)
            else:
                raise ValueError('input_path_list does not have the same \
                                  length than output_path_list')
        else:
            # Default prefix will be used
            pass
