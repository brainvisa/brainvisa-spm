# -*- coding: utf-8 -*-
from __future__ import absolute_import
import tempfile
from soma.spm.spm_batch_maker_utils import addBatchKeyWordInEachItem, moveFileAndCreateFoldersIfNeeded
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed, checkIfArgumentTypeIsStrOrUnicode

class ImageCalculator(object):
  """
  The  image calculator is for performing user-specified algebraic manipulations on
  a  set  of  images,  with  the  result  being  written  out  as  an image. The user is
  prompted  to supply images to work on, a filename for the output image, and the
  expression to evaluate. The expression should be a standard MATLAB expression,
  within which the images should be referred to as i1, i2, i3,... etc.
  """

  @checkIfArgumentTypeIsAllowed(list, 1)
  def setInputImagePathList(self, image_path_list):
    """
    These  are  the images that are used by the calculator.  They are referred to as i1,
    i2, i3, etc in the order that they are specified.
    """
    self.input_path_list = image_path_list

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setOutputImagePath(self, image_path):
    """
    The  output  image  is  written  to  current  working  directory  unless  a valid full
    pathname  is  given. If a path name is given here, the output directory setting will
    be ignored.
    """
    if image_path.split('.')[-1] != "nii":
        self.real_output_path =  image_path
        self.output_path = tempfile.NamedTemporaryFile(suffix=".nii").name
    else:
        self.output_path = image_path
        self.real_output_path = None


  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setOutputDirectory(self, directory_path):
    """
    Files  produced  by  this  function  will  be written into this output directory. If no
    directory  is  given,  images  will  be  written to current working directory. If both
    output  filename  and  output  directory  contain a directory, then output filename
    takes precedence.
    """
    self.output_directory = directory_path

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setExpression(self, expression):
    """
    Example expressions (f):
        * Mean of six images (select six images)
          f = '(i1+i2+i3+i4+i5+i6)/6'
        * Make a binary mask image at threshold of 100
          f = 'i1>100'
        * Make a mask from one image and apply to another
          f = 'i2.*(i1>100)'
          - here  the  first image is used to make the mask, which is applied to the
            second image
        * Sum of n images
          f = 'i1 + i2 + i3 + i4 + i5 + ...'
        * Sum of n images (when reading data into a data-matrix - use dmtx arg)
          f = 'sum(X)'
    """
    self.expression = expression

  def replaceOptions(self, options):
    self.options = options

  def getStringListForBatch( self ):
    if not None in [self.input_path_list, self.expression]:
      batch_list = []
      image_path_list_for_batch = []
      for image_path in self.input_path_list:
        image_path_list_for_batch.append("'%s,1'" % image_path)
      image_path_for_batch = '\n'.join(image_path_list_for_batch)

      batch_list.append("spm.util.imcalc.input = {%s};" %image_path_for_batch)
      batch_list.append("spm.util.imcalc.output = '%s';" %self.output_path)
      batch_list.append("spm.util.imcalc.outdir = {'%s'};" %self.output_directory)
      batch_list.append("spm.util.imcalc.expression = '%s';" %self.expression)
      batch_list.extend(addBatchKeyWordInEachItem("spm.util.imcalc", self.options.getStringListForBatch()))
      return batch_list
    else:
      raise ValueError("Missing input_path_list and/or expression")

  def _moveSPMDefaultPathsIfNeeded(self):
      if self.real_output_path is not None:
          moveFileAndCreateFoldersIfNeeded(self.output_path,
                                           self.real_output_path)
      else:
          pass#output is already in Nifti format