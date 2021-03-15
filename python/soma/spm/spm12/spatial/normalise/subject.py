# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, \
                                              checkIfArgumentTypeIsStrOrUnicode
from soma.spm.spm_batch_maker_utils import convertPathListToSPMBatchString, \
                                           moveSPMPath
from soma import aims

import abc
import six


class Subject(six.with_metaclass(abc.ABCMeta)):
    pass


class SubjectToEstimate(Subject):
    def __init__(self):
        self.images_to_align = None
        self.forward_deformation_field = None
    
    @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
    def setImagesToAlign(self, image_path):
        self.images_to_align = image_path

    def setForwardDeformationField(self, image_path):
        self.forward_deformation_field = image_path
        
    def getStringListForBatch(self):
        if self.images_to_align is None:
            raise ValueError('Images_to_align is mandatory')
            
        batch_list = []
        batch_list.append("vol = {'%s,1'};" % self.Images_to_align)

        return batch_list
        

class SubjectToEstimateAndWrite(SubjectToEstimate):
    def __init__(self):
        SubjectToEstimate.__init__(self)
        self.images_to_write = None
        self.images_written = None
        self.is4d = False

    @checkIfArgumentTypeIsAllowed(list, 1)
    def setImageListToWrite(self, image_path_list):
        if len(image_path_list) == 1:
            #TODO: handle case where multiple 4D files are provided
            image_volume = aims.read(image_path_list[0])
            if len(image_volume.shape) == 4 and image_volume.shape[-1] != 1:
                self.is4d = True
                self.images_to_write = \
                    [image_path_list[0] + ',' + str(index) 
                     for index in range(1, image_volume.shape[-1] + 1)]
            else:
                self.images_to_write = image_path_list
        else:
            self.images_to_write = image_path_list
        
    @checkIfArgumentTypeIsAllowed(list, 1)
    def setImageListWritten(self, image_path_list):
        self.images_written = image_path_list
    
    def getStringListForBatch(self):
        if None in [self.images_to_write, self.images_to_write]:
            raise ValueError(
                'Images_to_align and images_to_write are mandatory')
                
        batch_list = []
        batch_list.append("vol = {'%s,1'};" % self.images_to_align)
        batch_list.append(
            "resample = {%s};" %convertPathListToSPMBatchString(
                self.images_to_write, add_dimension=not(self.is4d)))
                
        return batch_list
        
    def movePathsIfNeeded(self, prefix):
        if self.images_written is not None:
            if not self.is4d:
                if len(self.images_to_write) == len(self.images_written):
                    for input_path, output_path in zip(self.images_to_write, 
                                                       self.images_written):
                        moveSPMPath(input_path,
                                    output_path,
                                    prefix=prefix)
                else:
                    raise ValueError('images_to_write does not have the same \
                                      length than images_written')
            else:
                if len(self.images_written) == 1:
                    moveSPMPath(self.images_to_write[0].split(',')[0],
                                self.images_written[0],
                                prefix=prefix)
                else:
                    raise ValueError('Too many images_written for 4D data.')
        else:
            # Default prefix will be used
            pass

        if self.forward_deformation_field is not None:
            moveSPMPath(self.images_to_align,
                        self.forward_deformation_field,
                        prefix='y_')
        

class SubjectToWrite(Subject):
    def __init__(self):
        self.deformation_field = None
        self.images_to_write = None
        self.images_written = None
        self.is4d = False

    @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
    def setDeformationField(self, deformation_field_path):
        self.deformation_field = deformation_field_path
        
    @checkIfArgumentTypeIsAllowed(list, 1)
    def setImageListToWrite(self, image_path_list):
        if len(image_path_list) == 1:
            #TODO: handle case where multiple 4D files are provided
            image_volume = aims.read(image_path_list[0])
            if len(image_volume.shape) == 4 and image_volume.shape[-1] != 1:
                self.is4d = True
                self.images_to_write = \
                    [image_path_list[0] + ',' + str(index) 
                     for index in range(1, image_volume.shape[-1] + 1)]
            else:
                self.images_to_write = image_path_list
        else:
            self.images_to_write = image_path_list
        
    @checkIfArgumentTypeIsAllowed(list, 1)
    def setImageListWritten(self, image_path_list):
        self.images_written = image_path_list
    
    def getStringListForBatch(self):
        if None in [self.deformation_field, self.images_to_write]:
            raise ValueError(
                'Deformation_field and images_to_write are mandatory')
                
        batch_list = []
        batch_list.append("def = {'%s'};" % self.deformation_field)
        batch_list.append(
            "resample = {%s};" %convertPathListToSPMBatchString(
                self.images_to_write, add_dimension=not(self.is4d)))
                
        return batch_list
        
    def movePathsIfNeeded(self, prefix):
        if self.images_written is not None:
            if not self.is4d:
                if len(self.images_to_write) == len(self.images_written):
                    for input_path, output_path in zip(self.images_to_write, 
                                                       self.images_written):
                        moveSPMPath(input_path,
                                    output_path,
                                    prefix=prefix)
                else:
                    raise ValueError('images_to_write does not have the same \
                                      length than images_written')
            else:
                if len(self.images_written) == 1:
                    moveSPMPath(self.images_to_write[0].split(',')[0],
                                self.images_written[0],
                                prefix=prefix)
                else:
                    raise ValueError('Too many images_written for 4D data.')
        else:
            # Default prefix will be used
            pass
