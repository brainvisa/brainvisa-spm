# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os

from soma.spm.virtual_spm.spatial.realign import EstimateAndReslice as EstimateAndReslice_virtual
from soma.spm.spm12.spatial.realign.estimation_options import EstimationOptions
from soma.spm.spm12.spatial.realign.reslice_options import ResliceOptions

from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
from soma.spm.spm_batch_maker_utils import convertPathListToSPMBatchString
from soma.spm.spm_batch_maker_utils import moveSPMPath
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed

from soma.spm.spm_main_module import SPM12MainModule
from soma import aims


class EstimateAndReslice(EstimateAndReslice_virtual, SPM12MainModule):
  def __init__(self):
    self.session_path_list = []
    self.session_realigned_path_list = []
    self.mean_output_path = None
    self.realignment_parameters_path_list = []

    self.estimation_options = EstimationOptions()
    self.reslice_options = ResliceOptions()
    

class EstimateAndReslice4d(EstimateAndReslice, SPM12MainModule):
    """
    For 4D images, the variable "data" in the batch is set differently than for
    3D images, with the 4D image path being repeated as many times as there are
    steps in the T direction.
    """
    
    @checkIfArgumentTypeIsAllowed(list, 1)
    def addSessionPathList(self, session_path_list):
        image_volume = aims.read(session_path_list[0])
        if len(image_volume.shape) != 4 or image_volume.shape[-1] == 1:
            raise RuntimeError('Input file is not in 4D.')
            
        self.session_path_list.append(
                    [session_path_list[0] + ',' + str(index) 
                     for index in range(1, image_volume.shape[-1] + 1)])
    
    def getStringListForBatch(self):
        if self.session_path_list:
            batch_list = []
            data_string = '{\n'
            for path_list in self.session_path_list:
                data_string += \
                    '{\n' + \
                    convertPathListToSPMBatchString(path_list, 
                                                    add_dimension=False) + \
                    '}\n'
            data_string += '}'
            batch_list.append(
                'spm.spatial.realign.estwrite.data = %s;' % data_string)
            batch_list.extend(addBatchKeyWordInEachItem(
                'spm.spatial.realign.estwrite', 
                self.estimation_options.getStringListForBatch()))
            batch_list.extend(addBatchKeyWordInEachItem(
                'spm.spatial.realign.estwrite', 
                self.reslice_options.getStringListForBatch()))
            return batch_list
        else:
            raise ValueError("At least one session is required")
    
    def _moveSPMDefaultPathsIfNeeded(self):
        reslice_choices = self.reslice_options.getReslicedImagesChoices()
        prefix = self.reslice_options.getCurrentFilenamePrefix()
        for index, path in enumerate(self.session_path_list):
            if self.session_realigned_path_list:
                moveSPMPath(path[0].split(',')[0], 
                            self.session_realigned_path_list[index][0], 
                            prefix=prefix)
    
            if self.realignment_parameters_path_list:
                moveSPMPath(path[0].split(',')[0], 
                            self.realignment_parameters_path_list[index], 
                            prefix="rp_", extension="txt")
    
        if reslice_choices[1] == 1:
            if self.mean_output_path is not None:
                moveSPMPath(self.session_path_list[0][0].split(',')[0], 
                            self.mean_output_path, prefix="mean")
    
    def moveSPMDefaultPathsFromTmpFolder(self, output_directory):
        reslice_choices = self.reslice_options.getReslicedImagesChoices()
        prefix = self.reslice_options.getCurrentFilenamePrefix()
        for index, path in enumerate(self.session_path_list):
            input_file_path = path[0].split(',')[0]
            
            realigned_path = os.path.join(output_directory, 
                                          prefix + os.path.basename(input_file_path))
            moveSPMPath(input_file_path, realigned_path, prefix=prefix)
    
            realignment_parameters_path = os.path.join(
                output_directory, 
                prefix + 'p_' + os.path.basename(input_file_path))
            realignment_parameters_path = '.'.join(
                realignment_parameters_path.split('.')[:-1] + ['txt'])
            moveSPMPath(input_file_path, realignment_parameters_path, 
                        prefix='rp_', extension='txt')
    
        if reslice_choices[1] == 1:
            input_file_path = self.session_path_list[0][0].split(',')[0]
            mean_path = os.path.join(output_directory, 
                                     'mean' + os.path.basename(input_file_path))
            moveSPMPath(input_file_path, mean_path, prefix='mean')
