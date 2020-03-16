# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsAllowed

class OneSampleTTestDesign(object):
  @checkIfArgumentTypeIsAllowed(list, 1)
  def setScans(self, scans):
    self.scans = scans
  
  def getStringListForBatch( self ):
    if self.scans is not None:
      batch_list = ["des.t1.scans = %s;" % self._buildStringAboutScansForBatch(self.scans)]
      return batch_list
    else:
      raise ValueError('OneSampleTTestDesign needs images list')

  def _buildStringAboutScansForBatch(self, scans_list):
      scans_path_list = []
      for scans in scans_list:
        scans_path_list.append("'%s,1'" % scans)
      return '{' + "\n".join(scans_path_list) + '}'