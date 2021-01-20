# -*- coding: utf-8 -*-
from __future__ import absolute_import
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsStrOrUnicode

class Contrast(object):
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setName(self, name):
    self.name = name
