# -*- coding: utf-8 -*-
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem, convertPathListToSPMBatchString, moveFileAndCreateFoldersIfNeeded
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode
import os

class Deformations():
  """
  This is a utility for working with deformation fields. They can be loaded, inverted, combined etc, and
  the results either saved to disk, or applied to some image.
  """
  def appendDeformation(self, deformation):
    raise NotImplementedError("This method will be overwritten in inherited classes")
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setCompositionName(self, composition_name):
    """
    Save the result as a three-volume image.  "y_" will be prepended to the filename.  The result will
    be written to the current directory.
    """
    self.composition_name = composition_name
    
  @checkIfArgumentTypeIsAllowed(list, 1)  
  def setImageListToDeform(self, image_path_list):
    self.image_path_list = image_path_list
  
  def setOuputDestinationToCurrentDirectory(self):
    self.output_destination = 'current directory'
    self.output_destination_path = None
  
  def setOuputDestinationToSourceDirectories(self):
    self.output_destination = 'source directory'
    self.output_destination_path = None
  
  def setOuputDestinationToDeformationDirectories(self):
    self.output_destination = 'deformation directory'
    self.output_destination_path = None
  
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setOuputDestination(self, output_path):
    self.output_destination = None
    self.output_destination_path = output_path
    
  def setInterpolationToNearestNeighbour(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    Nearest Neighbour:
          - Fastest, but not normally recommended.
    """
    self.interpolation = 0
    
  def setInterpolationToTrilinear(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    Trilinear Interpolation:
          - OK for PET, realigned fMRI, or segmentations
    """
    self.interpolation = 1
    
  def setInterpolationTo2ndDegreeBSpline(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
          - Better  quality (but slower) interpolation, especially with higher degree splines. Can produce
            values  outside  the  original range (e.g. small negative values from an originally all positive
            image).
    """
    self.interpolation = 2
    
  def setInterpolationTo3rdDegreeBSpline(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
          - Better  quality (but slower) interpolation, especially with higher degree splines. Can produce
            values  outside  the  original range (e.g. small negative values from an originally all positive
            image).
    """
    self.interpolation = 3
    
  def setInterpolationTo4thDegreeBSpline(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
          - Better  quality (but slower) interpolation, especially with higher degree splines. Can produce
            values  outside  the  original range (e.g. small negative values from an originally all positive
            image).
    """
    self.interpolation = 4
    
  def setInterpolationTo5thDegreeBSpline(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
          - Better  quality (but slower) interpolation, especially with higher degree splines. Can produce
            values  outside  the  original range (e.g. small negative values from an originally all positive
            image).
    """
    self.interpolation = 5
    
  def setInterpolationTo6thDegreeBSpline(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
          - Better  quality (but slower) interpolation, especially with higher degree splines. Can produce
            values  outside  the  original range (e.g. small negative values from an originally all positive
            image).
    """
    self.interpolation = 6
    
  def setInterpolationTo7thDegreeBSpline(self):
    """
    The method by which the images are sampled when being written in a different space. (Note that
    Inf or NaN values are treated as zero, rather than as missing data)
    B-spline Interpolation:
          - Better  quality (but slower) interpolation, especially with higher degree splines. Can produce
            values  outside  the  original range (e.g. small negative values from an originally all positive
            image).
    """
    self.interpolation = 7
    
  def getStringListForBatch( self ):
    if self.composition:
      if self.image_path_list:
        volume_path_for_batch = '{' + convertPathListToSPMBatchString(self.image_path_list) + '}'
      else:
        volume_path_for_batch = ''
      
      batch_list = []
      batch_list.extend(addBatchKeyWordInEachItem("spm.util.defs", self.composition.getStringListForBatch()))
      batch_list.append("spm.util.defs.ofname = '%s';" %self.composition_name)
      batch_list.append("spm.util.defs.fnames = %s;" %volume_path_for_batch)
      if self.output_destination == "current directory":
        batch_list.append("spm.util.defs.savedir.savepwd = 1;")
      elif self.output_destination == "source directory":
        batch_list.append("spm.util.defs.savedir.savesrc = 1;")
      elif self.output_destination == "deformation directory":
        batch_list.append("spm.util.defs.savedir.savedef = 1;")
      elif self.output_destination_path is not None:
        batch_list.append("spm.util.defs.savedir.saveusr = {'%s'};" %self.output_destination_path)
      else:
        raise ValueError("Unknown output combinaison")
      batch_list.append("spm.util.defs.interp = %i;" %self.interpolation)
    return batch_list
    
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setCompositionOutputPath(self, composition_path):
    self.composition_path = composition_path
    
  @checkIfArgumentTypeIsAllowed(list, 1)  
  def setImageListDeformed(self, image_path_list):
    self.deformed_image_path_list = image_path_list
  
  def _moveSPMDefaultPathsIfNeeded(self):
    self._moveCompositionIfNeeded()
    self._moveImageListDeformedIfNeeded()
      
  def _moveCompositionIfNeeded(self):
    if self.composition_path is not None and self.composition_name:
      filename = "y_" + self.composition_name + ".nii"#extension ".nii" is specified in SPM manual
      output_directory = self._getOutputDirectoryAboutComposition()
      spm_default_path = os.path.join(output_directory, filename)
      
      moveFileAndCreateFoldersIfNeeded(spm_default_path, self.composition_path)
    
  def _moveImageListDeformedIfNeeded(self):
    if self.deformed_image_path_list is not None:
      if len(self.image_path_list) == len(self.deformed_image_path_list):
        output_directory = self._getOutputDirectoryAboutImagesDeformed()
        for input_path, output_path in zip(self.image_path_list, self.deformed_image_path_list):
          spm_default_path = os.path.join(output_directory, 'w' + os.path.basename(input_path))
          moveFileAndCreateFoldersIfNeeded(spm_default_path, output_path)
    else:
      pass#SPM default
  
  def _getOutputDirectoryAboutComposition(self):
    if self.output_destination_path is not None:
      output_directory = self.output_destination_path
    elif self.output_destination == "current directory":
      raise NotImplementedError()#current directory is batch directory ?
    elif self.output_destination in ["source directory", "deformation directory"]:
      output_directory = os.path.dirname(self.composition.getFirstDeformationPath())
    else:
      raise ValueError("Unknown output combinaison")
    return output_directory
  
  def _getOutputDirectoryAboutImagesDeformed(self):
    if self.output_destination_path is not None:
      output_directory = self.output_destination_path
    elif self.output_destination == "current directory":
      raise NotImplementedError()#current directory is batch dirctory
    elif self.output_destination == "source directory":
      if self.image_path_list:
        output_directory = os.path.dirname(self.image_path_list[0])
      else:
        raise ValueError("Output directory can not be sources directory if not sources paths")
    elif self.output_destination == "deformation directory":
      output_directory = os.path.dirname(self.composition.getFirstDeformationPath())
    else:
      raise ValueError("Unknown output combinaison")
    return output_directory