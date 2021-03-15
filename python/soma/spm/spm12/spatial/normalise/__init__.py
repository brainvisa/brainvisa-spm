# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.virtual_spm.spatial.normalise import Estimate as Estimate_virtual
from soma.spm.virtual_spm.spatial.normalise import Write as Write_virtual
from soma.spm.virtual_spm.spatial.normalise \
    import EstimateAndWrite as EstimateAndWrite_virtual
from soma.spm.spm12.spatial.normalise.subject_container import SubjectContainer
from soma.spm.spm12.spatial.normalise.estimation_options \
    import EstimationOptions
from soma.spm.spm12.spatial.normalise.writing_options import WritingOptions

from soma.spm.spm_main_module import SPM12MainModule

class Estimate(Estimate_virtual, SPM12MainModule):
    def __init__(self):
        self.subject_container = SubjectContainer()
        self.estimation_options = EstimationOptions()

    @checkIfArgumentTypeIsAllowed(EstimationOptions, 1)
    def replaceEstimateOptions(self, estimation_options):
        del self.estimation_options
        self.estimation_options = estimation_options

#    def getStringListForBatch(self):
#        batch_list = []
#        batch_list.extend(addBatchKeyWordInEachItem(
#            'spm.spatial.normalise.est', 
#            self.subject_container.getStringListForBatch()))
#        batch_list.extend(addBatchKeyWordInEachItem(
#            'spm.spatial.normalise.est', 
#            self.estimation_options.getStringListForBatch()))
#            
#        return batch_list
#===============================================================================
#
#===============================================================================
class Write(Write_virtual, SPM12MainModule):
    def __init__(self):
        self.subject_container = SubjectContainer()
        self.writing_options = WritingOptions()
        
    @checkIfArgumentTypeIsAllowed(WritingOptions, 1)
    def replaceWritingOptions(self, writing_options):
        del self.writing_options
        self.writing_options = writing_options

#    def getStringListForBatch(self):
#        batch_list = []
#        batch_list.extend(addBatchKeyWordInEachItem(
#            'spm.spatial.normalise.write', 
#            self.subject_container.getStringListForBatch()))
#        batch_list.extend(addBatchKeyWordInEachItem(
#            'spm.spatial.normalise.write', 
#            self.writing_options.getStringListForBatch()))
#        
#        return batch_list
#===============================================================================
#
#===============================================================================
class EstimateAndWrite(EstimateAndWrite_virtual, SPM12MainModule):
    def __init__(self):
        self.subject_container = SubjectContainer()
        self.estimation_options = EstimationOptions()
        self.writing_options = WritingOptions()

#    def getStringListForBatch(self):
#        batch_list = []
#        batch_list.extend(addBatchKeyWordInEachItem(
#            "spm.spatial.normalise.estwrite", 
#            self.subject_container.getStringListForBatch()))
#        batch_list.extend(addBatchKeyWordInEachItem(
#            "spm.spatial.normalise.estwrite", 
#            self.estimation_options.getStringListForBatch()))
#        batch_list.extend(addBatchKeyWordInEachItem(
#            "spm.spatial.normalise.estwrite", 
#            self.writing_options.getStringListForBatch()))
#        return batch_list
