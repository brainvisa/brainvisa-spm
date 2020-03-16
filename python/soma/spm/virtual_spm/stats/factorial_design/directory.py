# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsStrOrUnicode

class Directory(object):
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setDirectory( self, directory_path ):
    if directory_path[-1] == '/':
      directory_path = directory_path[:-1]
    self.directory = directory_path
    
  def getStringListForBatch( self ):
    if self.directory is not None:
      batch_list = ["dir = {'%s/'};" % self.directory]
      return batch_list
    else:
      raise ValueError('Directory path is mandatory')