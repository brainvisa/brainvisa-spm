# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.virtual_spm.stats.factorial_design.directory import Directory as Directory_virtual

class Directory(Directory_virtual):
  def __init__(self):
    self.directory = None
