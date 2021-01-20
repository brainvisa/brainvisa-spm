from __future__ import absolute_import
from soma.spm.spm_main_module import SPM12MainModule
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem

from soma.spm.spm12.tools.cat12.estimation_options import EstimationOptions
from soma.spm.spm12.tools.cat12.extended_options import ExtendedOptions
from soma.spm.spm12.tools.cat12.writing_options import WritingOptions


class EstimateAndWrite(SPM12MainModule):
    def __init__(self):
        self.volume_path_list = None
        self.estimate_options = EstimationOptions()
        self.extended_options = ExtendedOptions()
        self.writing_options = WritingOptions()
        
    def getStringListForBatch(self):
        if self.volume_path_list is not None: 
            volume_path_list_for_batch = [] 
            for volume_path in self.volume_path_list:
                volume_path_list_for_batch.append("'%s'" % volume_path)
            volume_path_for_batch = '\n'.join(volume_path_list_for_batch)
            batch_list = []
            batch_list.append("spm.tools.cat.estwrite.data = {%s};" % volume_path_for_batch)
            batch_list.extend(addBatchKeyWordInEachItem("spm.tools.cat.estwrite",
                                                        self.estimate_options.getStringListForBatch()))
            batch_list.extend(addBatchKeyWordInEachItem("spm.tools.cat.estwrite",
                                                        self.extended_options.getStringListForBatch()))
            batch_list.extend(addBatchKeyWordInEachItem("spm.tools.cat.estwrite",
                                                        self.writing_options.getStringListForBatch()))
            return batch_list
        else:
            raise ValueError('At least one volume path is required')
