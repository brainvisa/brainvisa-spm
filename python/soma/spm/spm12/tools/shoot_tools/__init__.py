from __future__ import absolute_import
from soma.spm.spm_main_module import SPM12MainModule
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem, moveSPMPath
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem


class RunShoot(SPM12MainModule):
    def __init__(self):
        self.images_path_list = None
        self.templates_path_list = None
        
        self.jacobian_output_path_list = None
        self.velocity_output_path_list = None
        self.deformation_output_path_list = None
        
    def getStringListForBatch(self):
        if self.images_path_list is not None: 
            images_path_list_for_batch = [] 
            for tissue_images_path_list in self.images_path_list:
                tissues_path_list = ["'%s,1'" % t for t in tissue_images_path_list]
                images_path_list_for_batch.append('\n'.join(tissues_path_list))
            images_path_batch = '\n'.join(['{\n%s\n}' % i for i in images_path_list_for_batch])
            
            templates_path_batch = '\n'.join("'%s'" % temp for temp in self.templates_path_list)
            
            batch_list = []
            batch_list.append("spm.tools.shoot.warp1.images = {%s};" % images_path_batch)
            batch_list.append("spm.tools.shoot.warp1.templates = {%s};" % templates_path_batch)
            return batch_list
        else:
            raise ValueError('At least one image path is required')
    
    def _moveSPMDefaultPathsIfNeeded(self):
        if self.jacobian_output_path_list:
            self._move_output_default_path(self.jacobian_output_path_list, 'j_')
        if self.velocity_output_path_list:
            self._move_output_default_path(self.velocity_output_path_list, 'v_')
        if self.deformation_output_path_list:
            self._move_output_default_path(self.deformation_output_path_list, 'y_')
    
    def _move_output_default_path(self, output_list, output_prefix):
        if output_list is not None:
            if len(output_list) == len(self.images_path_list[0]):
                
                for src, dest in zip(self.images_path_list[0], output_list):
                    moveSPMPath(src, dest,
                                prefix=output_prefix,
                                suffix='_Template')
            else:
                raise ValueError("output_list has not the same length than images_path_list")
