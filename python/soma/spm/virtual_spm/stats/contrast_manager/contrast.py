# -*- coding: utf-8 -*-
from soma.spm.custom_decorator_pattern import checkIfArgumentTypeIsStrOrUnicode

class Contrast():
  @checkIfArgumentTypeIsStrOrUnicode(argument_index=1)
  def setName(self, name):
    self.name = name
