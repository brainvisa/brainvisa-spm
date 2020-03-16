 # -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
from soma.spm.spm_batch_maker_utils import convertPathListToSPMBatchString, moveSPMPath
from six.moves import zip

class SubjectToEstimate(object):
  """
  Data for this subject.  The same parameters are used within subject.
  """
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setSourceImage(self, image_path):
    self.source_image_path = image_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setSourceWeightingImage(self, image_path):
    self.source_weighting_image_path = image_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setSnMatOutputPath(self, sn_mat_filepath):
      self.sn_mat_filepath = sn_mat_filepath

  def getStringListForBatch(self):
    if self.source_image_path is not None:
      batch_list = []
      batch_list.append("source = {'%s,1'};" % self.source_image_path)
      if self.source_weighting_image_path:
        batch_list.append("wtsrc = {'%s,1'};" % self.source_weighting_image_path)
      else:
        batch_list.append("wtsrc = '';")
      return batch_list
    else:
      raise ValueError("source_image_path is mandatory")

  def movePathsIfNeeded(self):
    if self.sn_mat_filepath is not None:
      moveSPMPath(self.source_image_path,
                  self.sn_mat_filepath,
                  suffix="_sn",
                  extension="mat")
    else:
      pass#default prefix is used

class SubjectToEstimateAndWrite(SubjectToEstimate):
  """
  Data for this subject.  The same parameters are used within subject.
  """
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setImageListToWrite(self, image_path_list):
    self.image_path_list_to_write = image_path_list

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setImageListWritten(self, image_path_list):
    self.image_path_list_written = image_path_list

  def getStringListForBatch(self):
    if not None in [self.source_image_path, self.image_path_list_to_write]:
      batch_list = []
      batch_list.append("source = {'%s,1'};" % self.source_image_path)
      if self.source_weighting_image_path:
        batch_list.append("wtsrc = {'%s,1'};" % self.source_weighting_image_path)
      else:
        batch_list.append("wtsrc = '';")
      batch_list.append("resample = {%s};" %convertPathListToSPMBatchString(self.image_path_list_to_write))
      return batch_list
    else:
      raise ValueError("source_image_path and image_path_list_to_write are mandatory")

  def movePathsIfNeeded(self, prefix):
    SubjectToEstimate.movePathsIfNeeded(self)
    if self.image_path_list_written is not None:
      if len(self.image_path_list_to_write) == len(self.image_path_list_written):
        for input_path, output_path in zip(self.image_path_list_to_write, self.image_path_list_written):
          moveSPMPath(input_path,
                      output_path,
                      prefix=prefix)
      else:
        raise ValueError("both input and output images has not the same length")
    else:
      pass#default prefix is used

class SubjectToWrite(object):
  """
  Data for this subject.  The same parameters are used within subject.
  """
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setParameterFile(self, parameter_path):
    self.parameter_path = parameter_path

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setImageListToWrite(self, image_path_list):
    self.image_path_list_to_write = image_path_list

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setImageListWritten(self, image_path_list):
    self.image_path_list_written = image_path_list

  def getStringListForBatch(self):
    if not None in [self.parameter_path, self.image_path_list_to_write]:
      batch_list = []
      batch_list.append("matname = {'%s'};" % self.parameter_path)
      batch_list.append("resample = {%s};" %convertPathListToSPMBatchString(self.image_path_list_to_write))
      return batch_list
    else:
      raise ValueError("parameter_path and image_path_list_to_write are mandatory")

  def movePathsIfNeeded(self, prefix):
    if self.image_path_list_written is not None:
      if len(self.image_path_list_to_write) == len(self.image_path_list_written):
        for input_path, output_path in zip(self.image_path_list_to_write, self.image_path_list_written):
          moveSPMPath(input_path,
                      output_path,
                      prefix=prefix)
      else:
        raise ValueError("both input and output images has not the same length")
    else:
      pass#default prefix is used