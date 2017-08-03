# -*- coding: utf-8 -*-
from soma.spm.virtual_spm.tools.dartel_tools.run_dartel.settings import Settings
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem
from soma.spm.spm_batch_maker_utils import moveSPMPath, moveFileAndCreateFoldersIfNeeded

import os

class RunDartel():
  """
  Run  the  DARTEL  nonlinear  image  registration  procedure.  This  involves  iteratively  matching  all  the  selected images to a template
  generated  from  their  own  mean.  A  series  of  Template*.nii  files  are generated, which become increasingly crisp as the registration
  proceeds.
  """
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setFirstImageList(self, images_list):
    """
    Select  the  images to be warped together. Multiple sets of images can be simultaneously registered. For example, the first set may be a
    bunch of grey matter images, and the second set may be the white matter images of the same subjects.
    """
    self.images_list_list.insert(0, images_list)
    
  @checkIfArgumentTypeIsAllowed(list, 1)
  def appendImageList(self, images_list):
    """
    Select  the  images to be warped together. Multiple sets of images can be simultaneously registered. For example, the first set may be a
    bunch of grey matter images, and the second set may be the white matter images of the same subjects.
    """
    self.images_list_list.append(images_list)
    
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setOutputFlowFieldPathList(self, output_flow_field_path_list):
    self.output_flow_field_path_list = output_flow_field_path_list
    
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setOutputTemplatePathList(self, output_template_path_list):
    self.output_template_path_list = output_template_path_list
    
  @checkIfArgumentTypeIsAllowed(Settings, 1)
  def setSettings(self, settings):
    del self.settings
    self.settings = settings

  def getStringListForBatch( self ):
    if self.images_list_list:
      images_batch = "{\n"
      for images_list in self.images_list_list:
        images_batch += "{\n"
        for images_path in images_list:
          images_batch += "'%s,1'\n" % images_path
        images_batch += "}\n"
      images_batch += "}'"
      batch_list = []
      batch_list.append("spm.tools.dartel.warp.images = %s;" % images_batch)
      batch_list.extend(addBatchKeyWordInEachItem("spm.tools.dartel.warp", self.settings.getStringListForBatch()))
      return batch_list
    else:
      raise ValueError('images_list_list not found')
    
  def _moveSPMDefaultPathsIfNeeded(self):
    if self.output_flow_field_path_list is not None:
      if len(self.images_list_list[0]) == len(self.output_flow_field_path_list):
        for volume_path, output_flow_field_path in zip(self.images_list_list[0], self.output_flow_field_path_list):
          moveSPMPath(volume_path,
                      output_flow_field_path, 
                      prefix=self.flow_field_prefix,
                      suffix='_' + self.settings.getTemplateBasename())
      else:
        raise ValueError("images_list_list length do not coincide with output_flow_field_path_list length")
    else:
      pass#no specific output paths
    
    if self.output_template_path_list is not None:
      if len(self.output_template_path_list) == self.settings.getOuterIterationNumber():
        first_path = self.images_list_list[0][0]
        first_path_directory = os.path.dirname(first_path)
        first_path_extension = first_path.split('.')[-1]
        for index, path in enumerate(self.output_template_path_list):
          template_filename = self.settings.getTemplateBasename() + '_' + str(index) + '.' + first_path_extension
          spm_template_path = os.path.join(first_path_directory, template_filename)
          moveFileAndCreateFoldersIfNeeded(spm_template_path, path)
      else:
        raise ValueError("Unvalid output_template_path_list length")
    else:
      pass
      
      
    
    
