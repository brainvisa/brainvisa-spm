# -*- coding: utf-8 -*-
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsStrOrUnicode


class WriteFilteredImages():
  """Write filtered images"""
  def __init__(self):
    self.basename = None

  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setBasename(self, basename):
    """Enter basename of output files 'spm?_????_<basename>.ext'."""
    self.basename = basename


class ThresholdedSPM(WriteFilteredImages):
  """Save filtered SPM{.} as an image."""
  def __init__(self):
    WriteFilteredImages.__init__(self)

  def getStringListForBatch( self ):
    if self.basename is not None:
      return ["write.tspm.basename = '%s';" % self.basename]
    else:
      raise ValueError('Unvalid basename')


class AllClustersBinary(WriteFilteredImages):
  """Save filetered SPM{.} as a binary image."""
  def __init__(self):
    WriteFilteredImages.__init__(self)

  def getStringListForBatch( self ):
    if self.basename is not None:
      return ["write.binary.basename = '%s';" % self.basename]
    else:
      raise ValueError('Unvalid basename')


class AllClustersNAry(WriteFilteredImages):
  """Save filtered SPM{.} as an n-ary image."""
  def __init__(self):
    WriteFilteredImages.__init__(self)

  def getStringListForBatch( self ):
    if self.basename is not None:
      return ["write.nary.basename = '%s';" % self.basename]
    else:
      raise ValueError('Unvalid basename')