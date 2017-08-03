# -*- coding: utf-8 -*-
from collections import deque #deque is python container with append and clear methods (and others...)

class SPMContainer(deque):
  def __init__(self, type_contained):
    self.type_contained = type_contained
    
  def append(self, item):
    if isinstance(item, self.type_contained):
      super(SPMContainer, self).append(item)
    else:
      raise ValueError("unvalid item type")
    
  def appendleft(self, item):
    if isinstance(item, self.type_contained):
      super(SPMContainer, self).appendleft(item)
    else:
      raise ValueError("unvalid item type")
    
  def extend(self, iterable):
    for item in iterable:
      if not isinstance(item, self.type_contained):
        raise ValueError("unvalid item type")
      else:
        pass
      super(SPMContainer, self).extend(iterable)
    
  def extendleft(self, iterable):
    for item in iterable:
      if not isinstance(item, self.type_contained):
        raise ValueError("unvalid item type")
      else:
        pass
      super(SPMContainer, self).extendleft(iterable)
      
  